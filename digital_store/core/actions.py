def get_or_none(classmodel, **kwargs):
    """
    Получить объект из бд или None
    """
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def is_ajax(request):
    """
    Ajax-метод или нет
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
