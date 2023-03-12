from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
 
from cart.models import OrderHistory
from shop.models import Product, Shop
from shop.views import get_context_paginator
from .models import Review
from .forms import ReviewForm


@login_required
def review_add(request, product_id):
    """
    Добавление отзыва к продукту
    """

    product = get_object_or_404(Product, pk=product_id)

    product_in_order = OrderHistory.objects.filter(
        product=product, user=request.user, review=False
        ).order_by('created_date').first()

    if product_in_order is None:
        messages.error(request, 'Вы не можете оставить отзыв. Либо вы'
                       ' его уже оставили, либо еще не приобрели товар.')
        return redirect('shop:product', product.id)

    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        product_in_order.review = True
        product_in_order.save()

        return redirect('shop:product', product.id)
    return redirect('shop:index')


def review_remove(request, review_id, product_id):
    """
    Удаление отзыва из продукта
    """

    ...


def reviews_product_list(request, product_id):
    """
    Список отзывов для продукта
    """

    ...


def reviews_shop_list(request, shop_id):
    """
    Список отзывов о всех продуктах магазина
    """

    shop = get_object_or_404(Shop, pk=shop_id)
    shop_reviews = (Review.objects.filter(product__shop=shop)
                    .select_related('user'))

    context = {
        'shop': shop,
        'shop_reviews': shop_reviews,
        'shop_reviews_exists': shop_reviews.exists(),
    }

    context.update(get_context_paginator(shop_reviews, request))

    return render(
        request,
        context=context,
        template_name='review/reviews_shop_list.html',
    )
