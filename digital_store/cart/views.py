from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from shop.models import Product, Item
from core.actions import get_or_none
from .models import Cart


@login_required
def add_to_cart(request, product_id):
    """
    Добавление продукта в корзину
    """

    product = get_object_or_404(Product, pk=product_id)
    product_in_user_cart = get_or_none(Cart, product=product)

    if len(product.item.filter(status='sale').all()) == 0:
        return redirect('shop:index')
    item = Item.objects.filter(product=product, status='sale').first()

    if product_in_user_cart is None:
        create_product = Cart.objects.create(
            user=request.user,
            product=product,
            price=product.price,
            full_price=product.price,
            count_items=1,
        )
        create_product.save()
        create_product.items.add(item)

    else:
        product_in_user_cart.count_items += 1
        product_in_user_cart.full_price += product.price
        product_in_user_cart.items.add(item)
        product_in_user_cart.save()
    item.status = 'in_cart'
    item.save()

    return redirect('shop:product', product.id)
