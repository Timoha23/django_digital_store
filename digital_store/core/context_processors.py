from shop.models import Shop


def get_user_have_shop(request):
    try:
        return {'user_have_shop': Shop.objects.filter(
                                  owner=request.user).exists()}
    except TypeError:
        return {'user_have_shop': None}


def get_user_is_staff(request):
    STAFF_ROLES = ('moderator', 'admin',)

    if request.user.is_authenticated and request.user.role in STAFF_ROLES:
        return {'is_staff': True}
    return {'is_staff': False}