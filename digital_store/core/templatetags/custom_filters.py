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
