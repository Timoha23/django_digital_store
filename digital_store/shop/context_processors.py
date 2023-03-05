from .models import Shop


def get_user_have_shop(request):
    try:
        return {'user_have_shop': Shop.objects.filter(owner=request.user).exists()}
    except TypeError:
        return {'user_have_shop': None}
