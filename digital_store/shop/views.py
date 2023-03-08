from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from digital_store.settings import MEDIA_ROOT
from moderation.models import ModerationHistory
from reviews.models import Review
from reviews.forms import ReviewForm
from .models import Shop, Product, Item
from .forms import ShopForm, ProductForm, ItemForm


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
                product = get_object_or_404(Product, id=kwargs.get('product_id'))
                if request.user == product.shop.owner:
                    return func(request, *args, **kwargs)
        elif 'item_id' in kwargs:
            if request.user.is_authenticated:
                item = get_object_or_404(Item, id=kwargs.get('item_id'))
                if request.user == item.product.shop.owner:
                    return func(request, *args, **kwargs)
        return redirect('shop:index')
    return wrapper


def get_context_paginator(queryset, request, is_products=None):
    if is_products:
        count_posts = 9
    else:
        count_posts = 10
    paginator = Paginator(queryset, count_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'page_obj': page_obj,
    }


###############################################################


def index(request):
    """
    Главная страница проекта
    """

    products = Product.objects.filter(status='Accept', visibile=True).order_by('-created_date')[:9]

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

    shop = get_object_or_404(Shop, id=shop_id)
    if request.user == shop.owner:
        products = Product.objects.filter(shop=shop)
    else:
        products = Product.objects.filter(shop=shop, status='Accept', 
                                          visibile=True)

    context = {
        'shop': shop,
        'products': products,
        'products_exists': products.exists(),
    }

    context.update(get_context_paginator(products, request, is_products=True))

    return render(request, context=context, template_name='shop/shop.html')


def shop_list(request):
    """
    Страница со всеми магазинами
    """

    shops = Shop.objects.filter(status='Accept')

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

    product = get_object_or_404(Product, pk=product_id)
    shop = Shop.objects.get(shop_in_product=product_id)
    items = Item.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)

    review_form = ReviewForm()

    context = {
        'shop': shop,
        'product': product,
        'items': items,
        'reviews': reviews,
        'review_form': review_form,
        'items_exists': items.exists(),
    }

    context.update(get_context_paginator(reviews, request))

    return render(
        request,
        context=context,
        template_name='shop/product.html'
    )


def product_list(request):
    """
    Страница со всеми продуктами
    """

    products = Product.objects.filter(status='Accept')

    context = {
        'products': products,
    }

    context.update(get_context_paginator(products, request, is_products=True))

    return render(
        request,
        context=context,
        template_name='shop/product_list.html'
    )


def cart(request):
    """
    Страница корзины
    """

    return render(request, template_name='users/cart.html')


@login_required
def create_shop(request):
    """
    Сраница создания магазина
    """

    form = ShopForm(request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        shop = form.save(commit=False)
 
        # ПЕРЕДЕЛАТЬ
        if shop.image._file is None:
            shop.image = MEDIA_ROOT + 'img/default/shop.jpg'

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
        shop.save()
        ModerationHistory.objects.filter(shop=shop, product=None).delete()
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


@login_required
def user_shops(request):
    """
    Просмотр магазинов для владельца
    """

    shops = Shop.objects.select_related('owner').filter(owner=request.user)
    # default_image = STATICFILES_DIRS[0] + 'img/defautl/shop.img'

    context = {
        'shops': shops,
        'shops_exists': shops.exists(),
        # 'default_image': default_image,
    }

    context.update(get_context_paginator(shops, request))
    return render(
        request,
        context=context,
        template_name='shop/user_shops.html',
    )


@owner_required
def delete_shop(request, shop_id):
    """
    Удаление магазина юзером
    """

    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)
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
        return redirect('shop:shop', shop_id)

    if form.is_valid():
        product = form.save(commit=False)
        product.shop = shop
        product.count = 0
        product.save()
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
        ModerationHistory.objects.filter(product=product).delete()
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


@owner_required
def delete_product(request, product_id):
    """
    Удаление продукта
    """

    product = get_object_or_404(Product, id=product_id)

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
        return redirect('shop:product', product.id)

    context = {
        'form': form,
        'product': product,
    }

    return render(
        request,
        context=context,
        template_name='shop/create_item.html'
    )


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
