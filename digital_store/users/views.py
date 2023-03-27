from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Avg, BooleanField, Case, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from cart.models import Order
from core.actions import is_ajax
from core.pagination import get_context_paginator
from shop.views import Product

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

    orders = (Order.objects
              .filter(order_history__user=request.user)
              .distinct()
              .prefetch_related('order_history__product__shop',
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

    favorite_products = (Product.objects
                         .filter(favorite__user=request.user)
                         .prefetch_related('category')
                         .select_related('shop__owner')
                         .annotate(avg_rating=Avg('review__rating'),
                                   is_favorite=Case(
                                        When(favorite__user=request.user,
                                             then=True),
                                        default=False,
                                        output_field=BooleanField()),
                                   in_cart=Case(
                                        When(cart__user=request.user,
                                             then=True),
                                        default=False,
                                        output_field=BooleanField(),
                                        )))

    context = {}

    context.update(get_context_paginator(favorite_products, request))

    return render(request, context=context,
                  template_name='users/favorites.html')


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
