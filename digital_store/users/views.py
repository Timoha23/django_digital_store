from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from shop.views import get_context_paginator, Product
from cart.models import Order
from core.actions import get_or_none
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
    print(username)
    return render(request, template_name='users/profile.html')


@login_required
def order_list(request):
    """
    Отображение списка покупок для юзера
    """

    orders = (Order.objects.filter(order_history__user=request.user)
              .distinct().prefetch_related('order_history__product__shop')
              .order_by('-created_date')
              )

    for o in orders:
        print(o.order_history.all())

    context = {
        'orders': orders,
    }
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

    context = {
    }

    context.update(get_context_paginator(favorite_products, request))

    return render(request, context=context,
                  template_name='users/favorites.html')


@login_required
def add_to_favorite(request, product_id):
    """
    Добавление продукта в избранное
    """

    product = get_object_or_404(Product, pk=product_id)

    if Favorite.objects.filter(user=request.user, product=product).exists():
        messages.error(request, 'Данный товар уже находится у вас в избранном')
        return redirect('users:favorites')
    else:
        Favorite.objects.create(user=request.user, product=product)
        messages.success(request, f'Товар {product.name} успешно добавлен в избранное.')
        return redirect('users:favorites')


def remove_from_favorite(request, product_id):
    """
    Удаление продукта из избранного
    """

    product = get_object_or_404(Product, pk=product_id)

    favorite_obj = get_or_none(Favorite, product=product, user=request.user)

    if favorite_obj:
        favorite_obj.delete()
        messages.success(request, f'Товар {product.name} успешно удален из избранного.')
        return redirect('users:favorites')
    else:
        messages.error(request, f'Товар {product.name} не неходится в избранном.')
        return redirect('users:favorites')
