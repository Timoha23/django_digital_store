from django.utils import timezone

from digital_store.settings import STAFF_ROLES
from shop.models import Shop
from cart.models import Cart


def get_user_have_shop(request):
    try:
        return {'user_have_shop': Shop.objects.filter(
                                  owner=request.user).exists()}
    except TypeError:
        return {'user_have_shop': None}


def get_user_is_staff(request):
    if request.user.is_authenticated and request.user.role in STAFF_ROLES:
        return {'is_staff': True}
    return {'is_staff': False}


def get_year(request):
    year = timezone.now().year
    return {'year': year}


def count_products_cart(request):
    """
    Проверка на пустоту корзины. Если не пуста возвращает количество
    продуктов в корзине
    """

    context = {'count_products_cart': None}
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        if cart.exists():
            context['count_products_cart'] = cart.count()
    return context
