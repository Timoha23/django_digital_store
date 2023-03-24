from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.cache import cache

from shop.views import Product
from cart.models import Order
from core.pagination import get_context_paginator
from core.actions import is_ajax
from .forms import CreationForm
from .models import Favorite


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('shop:index')
    template_name = 'users/signup.html'


def user_profile(request, username):
    """
    Профиль пользователя
    """

    return render(request, template_name='users/profile.html')


@login_required
def order_list(request):
    """
    Отображение списка покупок для юзера
    """

    orders = (Order.objects.filter(order_history__user=request.user)
              .distinct().prefetch_related('order_history__product__shop',
                                           'order_history__items')
              .order_by('-created_date')
              )

    context = {}

    context.update(get_context_paginator(orders, request))

    return render(request, context=context, template_name='users/orders.html')


@login_required
def get_favorite_list(request):
    """
    Получить список избранных продуктов
    """

    favorite_products = (Product.objects.filter(favorite__user=request.user)
                         .prefetch_related('category')
                         .select_related('shop__owner')
                         )

    if request.user.is_authenticated:
        favorites = request.user.favorite.all().values_list('product__id',
                                                            flat=True)
        cart = request.user.cart.all().values_list('product__id',
                                                   flat=True)
    else:
        favorites = []
        cart = []

    context = {
        'favorites': favorites,
        'cart': cart,
    }

    context.update(get_context_paginator(favorite_products, request))

    return render(request, context=context,
                  template_name='users/favorites.html')


# @login_required
# def add_to_favorite(request, product_id):
    # """
    # Добавление продукта в избранное
    # """

    # product = get_object_or_404(Product, pk=product_id)

    # if request.user == product.shop.owner:
    #     messages.error(request, 'Владелец не может добавить свой товар в избранное.')
    #     return redirect('users:favorites')
    # if Favorite.objects.filter(user=request.user, product=product).exists():
    #     messages.error(request, 'Данный товар уже находится у вас в избранном')
    #     return redirect('users:favorites')
    # else:
    #     Favorite.objects.create(user=request.user, product=product)
    #     messages.success(request, f'Товар {product.name} успешно добавлен в избранное.')
    #     return redirect('users:favorites')


@login_required
def change_favorite(request):
    """
    Удаление/добавление продукта из избранного
    """

    if is_ajax(request=request) and request.method == 'POST':
        data = request.POST
        is_favorite = False
        product = get_object_or_404(Product, id=int(data['product_id']))
        fav_obj = Favorite.objects.filter(user=request.user, product=product)
        if fav_obj.exists():
            fav_obj.first().delete()
        else:
            Favorite.objects.create(user=request.user, product=product)
            is_favorite = True

        context = {
            'is_favorite': is_favorite,
        }

        cache.clear()
        return JsonResponse(context, safe=False)
    return JsonResponse({"success": False}, status=400)
