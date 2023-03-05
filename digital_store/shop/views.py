from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from digital_store.settings import MEDIA_ROOT
from .models import Shop, Product, Item
from .form import ShopForm, ProductForm, ItemForm


def index(request):
    """
    Главная страница проекта
    """

    products = Product.objects.all().order_by('-created_date')
    print(products.first().shop.owner)

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
    products = Product.objects.filter(shop=shop)

    context = {
        'shop': shop,
        'products': products,
        'products_exists': products.exists(),
    }

    return render(request, context=context, template_name='shop/shop.html')


def product(request, product_id):
    """
    Страница продукта
    """
    product = get_object_or_404(Product, pk=product_id)
    shop = Shop.objects.get(shop_in_product=product_id)
    items = Item.objects.filter(product=product)

    context = {
        'shop': shop,
        'product': product,
        'items': items,
        'items_exists': items.exists(),
    }

    return render(
        request,
        context=context,
        template_name='shop/product.html'
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


def edit_shop(request, shop_id):
    """
    Редактирование магазина
    """
    shop = get_object_or_404(Shop, pk=shop_id)
    form = ShopForm(request.POST or None,
                    files=request.FILES or None,
                    instance=shop)
    if shop.owner != request.user:
        return redirect('shop:index')
    if form.is_valid():
        form.save()
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

    shops = Shop.objects.filter(owner=request.user)
    # default_image = STATICFILES_DIRS[0] + 'img/defautl/shop.img'

    context = {
        'shops': shops,
        'shops_exists': shops.exists(),
        # 'default_image': default_image,
    }

    return render(
        request,
        context=context,
        template_name='shop/user_shops.html',
    )


def delete_shop(request, shop_id):
    """
    Удаление магазина юзером
    """

    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)
    shop.delete()
    return redirect('shop:index')


def create_product(request, shop_id):
    """
    Создание подукта
    """

    form = ProductForm(request.POST or None,
                       files=request.FILES or None)

    shop = Shop.objects.get(id=shop_id)

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


def edit_product(request, shop_id, product_id):
    """
    Редактирование продукта
    """
    product = get_object_or_404(Product, pk=product_id)
    shop = product.shop
    form = ProductForm(request.POST or None,
                       files=request.FILES or None,
                       instance=product)

    if product.shop.owner != request.user:
        return redirect('shop:index')
    if form.is_valid():
        form.save()
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


def delete_product(request, product_id):
    """
    Удаление продукта
    """

    product = get_object_or_404(Product, id=product_id)

    if product.shop.owner == request.user:
        product.delete()
        return redirect('shop:shop', product.shop.id)
    return redirect('shop:index')


def create_item(request, product_id):
    """
    Добавление товара в продукт
    """

    form = ItemForm(request.POST or None)
    product = get_object_or_404(Product, id=product_id)

    if form.is_valid():
        item = form.save(commit=False)
        item.product = product
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


def delete_item(request, item_id):
    """
    Удаление товара из продукта
    """

    item = get_object_or_404(Item, id=item_id)
    if item.product.shop.owner == request.user:
        item.delete()
        return redirect('shop:product', item.product.id)
    return redirect('shop:index')
