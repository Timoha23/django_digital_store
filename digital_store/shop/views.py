from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, BooleanField, Case, When
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST

from cart.models import OrderHistory
from core.pagination import get_context_paginator
from digital_store.settings import CACHE_TIME, STAFF_ROLES
from moderation.models import AcceptRejectList
from reviews.forms import ReviewForm
from reviews.models import Review

from .forms import ItemForm, ProductForm, ShopForm
from .models import Category, Item, Product, Shop


def get_products(request):
    """
    Получение продуктов без фильтров
    """
    products = (Product.objects
                .filter()
                .select_related('shop__owner')
                .prefetch_related('category', 'review')
                .order_by('-is_available', '-created_date')
                .annotate(avg_rating=Avg('review__rating'))
                )
    if request.user.is_authenticated:
        products = products.annotate(is_favorite=Case(
                            When(favorite__user=request.user,
                                 then=True),
                            default=False,
                            output_field=BooleanField()),
                          in_cart=Case(
                              When(cart__user=request.user,
                                   then=True),
                              default=False,
                              output_field=BooleanField(),
                      ))

    return products


def owner_required(func):
    """
    Декоратор. Проверка является ли юзер владельцем магазина
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'shop_id' in kwargs:
            if request.user.is_authenticated:
                shop = get_object_or_404(Shop, id=kwargs.get('shop_id'))
                if request.user == shop.owner:
                    return func(request, *args, **kwargs)
        elif 'product_id' in kwargs:
            if request.user.is_authenticated:
                product = get_object_or_404(Product,
                                            id=kwargs.get('product_id'))
                if request.user == product.shop.owner:
                    return func(request, *args, **kwargs)
        elif 'item_id' in kwargs:
            if request.user.is_authenticated:
                item = get_object_or_404(Item, id=kwargs.get('item_id'))
                if request.user == item.product.shop.owner:
                    return func(request, *args, **kwargs)
        return redirect('shop:index')
    return wrapper


###############################################################


@cache_page(CACHE_TIME)
def index(request):
    """
    Главная страница проекта
    """

    products = (get_products(request)
                .filter(status='Accept', visibile=True)
                )

    context = {
        'products': products,
    }

    return render(
        request,
        context=context,
        template_name='shop/index.html'
    )


def shop(request, shop_id):
    """
    Страница магазина
    """

    shop = get_object_or_404(
        (Shop.objects
         .annotate(avg_rating=Avg('products__review__rating'))
         .select_related('owner')),
        id=shop_id)

    # проверка статуса магазина
    if shop.status != 'Accept':
        if request.user.is_authenticated is True:
            if (request.user != shop.owner or request.user.role
                    not in STAFF_ROLES):
                raise Http404
        else:
            raise Http404

    products = get_products(request)
    if not request.user.is_authenticated or request.user != shop.owner:
        products = products.filter(
                status='Accept',
                visibile=True,
                is_available=True
            )
    products = products.filter(shop=shop)

    context = {
        'shop': shop,
        'products': products,
        'products_exists': products.exists(),
    }

    context.update(get_context_paginator(products, request, is_products=True))

    return render(request, context=context, template_name='shop/shop.html')


@cache_page(CACHE_TIME)
def shop_list(request):
    """
    Страница со всеми магазинами
    """

    shops = (Shop.objects.filter(status='Accept')
             .select_related('owner')
             .annotate(avg_rating=Avg('products__review__rating'))
             .order_by('-created_date'))

    context = {
        'shops': shops,
    }

    context.update(get_context_paginator(shops, request))
    return render(
        request,
        context=context,
        template_name='shop/shop_list.html'
    )


def product(request, product_id):
    """
    Страница продукта
    """

    can_review = False

    if Product.objects.filter(pk=product_id).exists():

        product = (Product.objects
                   .filter(pk=product_id)
                   .select_related('shop__owner')
                   .annotate(
                        avg_rating=Avg('review__rating'),
                    ))
        if request.user.is_authenticated:
            product = product.annotate(is_favorite=Case(
                    When(favorite__user=request.user,
                         then=True),
                    default=False,
                    output_field=BooleanField()),
                in_cart=Case(
                    When(cart__user=request.user,
                         then=True),
                    default=False,
                    output_field=BooleanField()))
            can_review = OrderHistory.objects.filter(
                product=product.first(),
                user=request.user,
                review=False
            )
    else:
        raise Http404
    product = product.first()
    shop = Shop.objects.get(products=product_id)
    items = Item.objects.filter(product=product, status='sale')
    reviews = (Review.objects.filter(product=product)
               .select_related('user')
               .order_by('-created_date'))
    review_form = ReviewForm()

    if product.status != 'Accept':
        if request.user.is_authenticated is True:
            if (request.user != shop.owner or
                    request.user.role not in STAFF_ROLES):
                raise Http404
        else:
            raise Http404

    context = {
        'shop': shop,
        'product': product,
        'items': items,
        'reviews': reviews,
        'review_form': review_form,
        'items_exists': items.exists(),
        'can_review': can_review,
    }

    context.update(get_context_paginator(reviews, request))

    return render(
        request,
        context=context,
        template_name='shop/product.html'
    )


@cache_page(CACHE_TIME)
def product_list(request):
    """
    Страница со всеми продуктами
    """

    products = (get_products(request)
                .filter(status='Accept', visibile=True)
                )

    context = {}
    context.update(get_context_paginator(products, request, is_products=True))

    return render(
        request,
        context=context,
        template_name='shop/product_list.html'
    )


@login_required
def create_shop(request):
    """
    Сраница создания магазина
    """

    form = ShopForm(request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        shop = form.save(commit=False)
        shop.owner = request.user
        shop.save()
        return redirect('shop:index')

    context = {
        'form': form,
    }
    return render(
        request,
        context=context,
        template_name='shop/create_shop.html'
    )


@owner_required
def edit_shop(request, shop_id):
    """
    Редактирование магазина
    """

    shop = get_object_or_404(Shop, pk=shop_id)
    form = ShopForm(request.POST or None,
                    files=request.FILES or None,
                    instance=shop)

    if form.is_valid():
        form.save()
        shop.status = 'In_Consideration'
        shop.save(delete=True)
        AcceptRejectList.objects.filter(shop=shop, product=None).delete()
        return redirect('shop:user_shops')
    context = {
        'edit_shop': True,
        'form': form,
        'shop_id': shop_id,
    }
    return render(
        request,
        context=context,
        template_name='shop/create_shop.html',
    )


@require_POST
@owner_required
def delete_shop(request, shop_id):
    """
    Удаление магазина юзером
    """

    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)

    # удаляем все ордеры связаныне с данным магазином (с его продуктами)
    for pr in shop.products.all():
        for o_h in pr.order_history.all():
            o_h.order.delete()
    shop.delete()
    return redirect('shop:index')


@owner_required
def create_product(request, shop_id):
    """
    Создание подукта
    """

    form = ProductForm(request.POST or None,
                       files=request.FILES or None)

    shop = get_object_or_404(Shop, id=shop_id)

    if shop.status != 'Accept':
        messages.error(request, f'Вы не можете добавить товар. '
                                f'Ваш магазин имеет статус: '
                                f'{shop.get_status_display()}.')
        return redirect('shop:shop', shop_id)

    if form.is_valid():
        product = form.save(commit=False)
        product.shop = shop
        product.count = 0
        product.save()
        form.save_m2m()
        return redirect('shop:shop', shop_id)

    context = {
        'form': form,
        'shop': shop,
    }

    return render(
        request,
        context=context,
        template_name='shop/create_product.html'
    )


@owner_required
def edit_product(request, shop_id, product_id):
    """
    Редактирование продукта
    """
    product = get_object_or_404(Product, pk=product_id)
    shop = product.shop
    form = ProductForm(request.POST or None,
                       files=request.FILES or None,
                       instance=product)

    if form.is_valid():
        form.save()
        product.status = 'In_Consideration'
        product.save()
        AcceptRejectList.objects.filter(product=product).delete()
        return redirect('shop:shop', shop_id)
    context = {
        'edit_product': True,
        'form': form,
        'product_id': product_id,
        'shop': shop,
    }
    return render(
        request,
        context=context,
        template_name='shop/create_product.html',
    )


@require_POST
@owner_required
def delete_product(request, product_id):
    """
    Удаление продукта
    """

    product = get_object_or_404(Product, id=product_id)

    # удаляем все ордеры связаныне с данным продуктом
    for o_h in product.order_history.all():
        o_h.order.delete()
    product.delete()
    return redirect('shop:shop', product.shop.id)


@owner_required
def create_item(request, product_id):
    """
    Добавление товара в продукт
    """

    form = ItemForm(request.POST or None)
    product = get_object_or_404(Product, id=product_id)

    if form.is_valid():
        item = form.save(commit=False)
        item.product = product
        product.count += 1
        product.save()
        item.save()
        return redirect('shop:shop', product.shop.id)

    context = {
        'form': form,
        'product': product,
    }

    return render(
        request,
        context=context,
        template_name='shop/create_item.html'
    )


@require_POST
@owner_required
def delete_item(request, item_id):
    """
    Удаление товара из продукта
    """

    item = get_object_or_404(Item, id=item_id)
    product = item.product
    product.count -= 1
    product.save()
    item.delete()
    return redirect('shop:product', item.product.id)


def search(request):
    """
    Поиск товаров
    """

    query = request.GET.get('query')

    products = get_products(request).filter(name__icontains=query,
                                            status='Accept',
                                            visibile=True,)

    context = {
        'query': query,
    }

    context.update(get_context_paginator(products, request, is_products=True))

    return render(request, context=context,
                  template_name='shop/search_product.html')


def category(request, slug):
    """
    Отображение товаров определенной категории
    """

    if not Category.objects.filter(slug=slug).exists():
        messages.error(request, f'Категории {slug} не существует')
        return redirect('shop:index')

    products = get_products(request).filter(category__slug=slug,
                                            status='Accept',
                                            visibile=True,)

    context = {
        'slug': slug,
    }
    context.update(get_context_paginator(products, request, is_products=True))

    return render(request, context=context, template_name='shop/category.html')
