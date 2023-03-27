from django.utils import timezone

from digital_store.settings import STAFF_ROLES
from shop.models import Shop


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
