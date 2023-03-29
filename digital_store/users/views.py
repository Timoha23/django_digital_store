from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Avg, BooleanField, Case, Count, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from cart.models import Order, OrderHistory
from core.actions import is_ajax
from core.pagination import get_context_paginator
from reviews.models import Review
from shop.models import Product, Shop
from shop.views import get_products

from .forms import CreationForm, ChangeProfileForm
from .models import Favorite, User


def _get_percent_rating(user) -> dict:
    """
    Получение процента по шкале рейтинга
    """

    stars_dict = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
    }

    stars_percent = {
        1: (0, 0),
        2: (0, 0),
        3: (0, 0),
        4: (0, 0),
        5: (0, 0),
    }

    reviews = Review.objects.filter(product__shop__owner=user).values('rating')

    if reviews.count() == 0:
        return stars_percent

    # заполняем словарь для подсчета каждой оценки
    for star in reviews:
        stars_dict[star['rating']] += 1

    # заполняем словарь для подсчета процента по оценкам
    for star in stars_dict:
        stars_percent[star] = (
            stars_dict[star], round((stars_dict[star] / reviews.count()) * 100)
        )
    return stars_percent


############################
class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('shop:index')
    template_name = 'users/signup.html'


def user_profile(request, username):
    """
    Профиль пользователя
    """

    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
        }
    if Shop.objects.filter(owner=user).exists():
        count_shops = Shop.objects.filter(owner=user, status='Accept').count()
        count_products = Product.objects.filter(
            shop__owner=user,
            status='Accept',
            is_available=True,
            visibile=True
        ).count()

        rating = (Review.objects
                  .filter(product__shop__owner=user)
                  .aggregate(Avg('rating'))
                  )

        rating = (int(rating.get('rating__avg'))
                  if (rating.get('rating__avg')) is not None else None)

        count_sales = (OrderHistory.objects
                       .filter(product__shop__owner=user)
                       .aggregate(Count('count_items'))
                       )

        context.update({
            'count_shops': count_shops,
            'count_products': count_products,
            'rating': rating,
            'count_sales': count_sales.get('count_items__count'),
            'percent_rating': _get_percent_rating(user),
        })
    return render(request, context=context, template_name='users/profile.html')


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
        return JsonResponse(context, status=200)
    return JsonResponse({"success": False}, status=400)


def get_user_shop_list(request, username):
    """
    Получаем все магазины данного юзера
    """

    if request.user.username == username:
        shops = Shop.objects.filter(owner__username=username)
    else:
        shops = Shop.objects.filter(owner__username=username,
                                    status='Accept')

    context = {}
    context.update(get_context_paginator(shops, request))
    return render(request, context=context,
                  template_name='shop/shop_list.html')


def get_user_product_list(request, username):
    """
    Получаем все товары(продукты) связанные с данным юзером
    """

    if request.user.username == username:
        products = get_products(request, all=True)
        products = products.filter(shop__owner__username=username)
    else:
        products = get_products(request)
        products = products.filter(shop__owner__username=username,
                                   visibile=True, status='Accept')
    context = {}
    context.update(get_context_paginator(products, request, is_products=True))
    return render(request, context=context,
                  template_name='shop/product_list.html')


def edit_profile(request):
    user = request.user
    form = ChangeProfileForm(request.POST or None,
                             files=request.FILES or None,
                             instance=user)
    if form.is_valid():
        form.save()
        return redirect('users:user_profile', user.username)

    context = {
        'form': form,
    }
    return render(request, context=context,
                  template_name='users/edit_profile.html')
