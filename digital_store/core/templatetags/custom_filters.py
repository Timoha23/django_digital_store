from django import template

register = template.Library()


@register.filter(name='custom_range')
def custom_range(rating):
    return range(rating)


@register.filter(name='is_available')
def is_available(count):
    if count == 0:
        return False
    return True


@register.filter(name='get_product_full_price')
def get_product_full_price(obj):
    """
    Расчет стоимости продукта в зависимости от его кол-ва
    """

    return obj.count_items * obj.product.price
