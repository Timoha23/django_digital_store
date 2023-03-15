from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse

from shop.models import Product, Item
from core.actions import get_or_none, is_ajax
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
            count_items=1,
        )
        create_product.save()

    else:
        product_in_user_cart.count_items += 1
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

    cart_price = 0

    cart = (Cart.objects.filter(user=request.user)
            .select_related('product', 'product__shop')
            )

    # расчет общей суммы корзины
    for obj in cart:
        cart_price += obj.count_items * obj.product.price

    context = {
        'cart': cart,
        'cart_price': cart_price,
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
        price = obj.product.price
        count_items = obj.count_items
        full_price = price * count_items
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


@login_required
def add_count_items(request):
    """
    Изменение количества товара в корзине(+)
    """

    # if is_ajax(request=request):
    if is_ajax(request=request) and request.method == 'POST':
        data = request.POST
        maximum_count = False
        obj = get_object_or_404(Cart, id=int(data['object_id']))
        full_cart_price = int(data['full_cart_price'])

        full_cart_price += obj.product.price
        obj.count_items += 1
        obj.save()

        if obj.count_items >= obj.product.count:
            maximum_count = True

        full_price = obj.product.price * obj.count_items
        context = {
            'maximum_count': maximum_count,
            'count_items': obj.count_items,
            'full_price': full_price,
            'full_cart_price': full_cart_price,
        }

        return JsonResponse(context, status=200)
    return JsonResponse({"success": False}, status=400)


@login_required
def remove_count_items(request):
    """
    Изменение количества товара в корзине(-)
    """

    if is_ajax(request=request) and request.method == 'POST':
        data = request.POST
        minimum_count = False
        obj = get_object_or_404(Cart, id=int(data['object_id']))
        full_cart_price = int(data['full_cart_price'])
        full_cart_price -= obj.product.price
        obj.count_items -= 1
        obj.save()

        if obj.count_items == 0:
            minimum_count = True

        full_price = obj.product.price * obj.count_items

        context = {
            'minimum_count': minimum_count,
            'count_items': obj.count_items,
            'full_price': full_price,
            'full_cart_price': full_cart_price,
        }

        return JsonResponse(context, status=200)
    return JsonResponse({"success": False}, status=400)
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
