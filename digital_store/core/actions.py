def get_or_none(classmodel, **kwargs):
    """
    Получить объект из бд или None
    """
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
