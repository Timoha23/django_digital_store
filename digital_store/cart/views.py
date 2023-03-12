from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from shop.models import Product, Item
from core.actions import get_or_none
from .models import Cart, Order, OrderHistory


@login_required
def add_to_cart(request, product_id):
    """
    Добавление продукта в корзину
    """

    product = get_object_or_404(Product.objects.filter(status='Accept'),
                                pk=product_id)
    product_in_user_cart = get_or_none(Cart, product=product)

    len_sale_products = len(product.item.filter(status='sale').all())


    # проверка то, что юзер хочет добавить товаров больше чем их есть в наличии
    if product_in_user_cart:
        if len_sale_products <= product_in_user_cart.count_items:
            messages.error(request, f'Недопустимое количество товара. В магазине всего: {len_sale_products}')
            return redirect('shop:index')

    if len_sale_products == 0:
        messages.error(request, 'Недостаточно товаров')
        return redirect('shop:index')


    if product_in_user_cart is None:
        create_product = Cart.objects.create(
            user=request.user,
            product=product,
            price=product.price,
            full_price=product.price,
            count_items=1,
        )
        create_product.save()

    else:
        product_in_user_cart.count_items += 1
        product_in_user_cart.full_price += product.price
        product_in_user_cart.save()

    return redirect('shop:product', product.id)


@login_required
def del_from_cart(request, product_id):
    """
    Удаление продукта из корзины
    """

    cart_obj = get_object_or_404(Cart, product__id=product_id, user=request.user)
    cart_obj.delete()
    messages.success(request, f'Товар {cart_obj.product.name} успешно удален из корзины.')
    return redirect('cart:cart')


@login_required
def cart(request):
    """
    Отображение продуктов в корзине
    """

    cart = (Cart.objects.filter(user=request.user)
            .select_related('product', 'product__shop')
            )

    cart_price = cart.aggregate(Sum('full_price')) or 0

    context = {
        'cart': cart,
        'cart_price': cart_price.get('full_price__sum') or 0,
    }

    return render(request, context=context, template_name='cart/cart.html')


@login_required
def make_order(request):
    cart = Cart.objects.filter(user=request.user)
    order = Order.objects.create()

    if len(cart) < 1:
        messages.error(request, 'В вашей корзине нет товаров')
        return redirect('cart:cart')

    for obj in cart:
        product = obj.product
        price = obj.price
        full_price = obj.full_price
        count_items = obj.count_items
        items = product.item.filter(status='sale')[:count_items]
        # проверка на то есть ли указаное в заказе количество товара
        if len(items) < count_items:
            messages.error(request, f'К сожалению {product.name} имеет в наличии только {len(items)} товаров. У вас указано {count_items}')
            return redirect('cart:cart')

        order_history = OrderHistory.objects.create(
            user=request.user,
            order=order,
            product=product,
            price=price,
            full_price=full_price,
            count_items=count_items,
        )
        for item in items:
            item.status = 'sold'
            item.save()

        order_history.items.set(items[:count_items])
        order_history.save()

        product.count -= len(items)
        product.save()

        cart.delete()

    messages.success(request, 'Заказ успешно оформлен!')

    return redirect('cart:cart')


# @login_required
# def order_list(request):
#     """
#     Отображение списка покупок для юзера
#     """

#     orders = (Order.objects.filter(order_history__user=request.user)
#               .distinct().prefetch_related('order_history__product')
#               .prefetch_related('order_history__product__shop')
#               )

#     context = {
#         'orders': orders,
#     }
#     return render(request, context=context, template_name='cart/orders.html')
