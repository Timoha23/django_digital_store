from django.shortcuts import render, redirect, get_object_or_404

from digital_store.settings import MEDIA_ROOT
from .models import Shop, Product
from .form import ShopForm, ProductForm, ItemForm


def index(request):
    """
    Вью главной страницы проекта
    """

    return render(request, template_name='shop/index.html')


def shop(request, shop_id):
    """
    Вью страницы магазина
    """

    shop = get_object_or_404(Shop, id=shop_id)
    products = Product.objects.filter(shop=shop)

    context = {
        'shop': shop,
        'products': products,
        'products_exists': products.exists(),
    }

    return render(request, context=context, template_name='shop/shop.html')


def product(request, item_id):
    """
    Вью страницы продукта
    """

    print(item_id)
    return render(request, template_name='shop/product.html')


def cart(request):
    """
    Втю страницы корзины
    """

    return render(request, template_name='users/cart.html')


def create_shop(request):
    """
    Вью траницы создания магазина
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
    Вью редактирование магазина
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


def user_shops(request):
    """
    Вью просмотр магазинов для владельца
    """
    shops = Shop.objects.filter(owner=request.user)
    # default_image = STATICFILES_DIRS[0] + 'img/defautl/shop.img'

    context = {
        'shops': shops,
        # 'default_image': default_image,
    }

    return render(
        request,
        context=context,
        template_name='shop/user_shops.html',
    )


def delete_shop(request, shop_id):
    """
    Вью для удаления магазина юзером
    """

    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)
    shop.delete()
    return redirect('shop:index')


def create_product(request, shop_id):
    """
    Вью создание подукта
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


def edit_product(request, product_id, shop_id):
    """
    Вью редактирование продукта
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
    Вью удаление продукта
    """

    product = get_object_or_404(Product, id=product_id)

    if product.shop.owner == request.user:
        product.delete()
        return redirect('shop:shop', product.shop.id)
    return redirect('shop:index')
