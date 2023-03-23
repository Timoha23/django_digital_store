from django.core.paginator import Paginator


def get_context_paginator(queryset, request, is_products=False):
    if is_products:
        count_posts = 9
    else:
        count_posts = 10
    paginator = Paginator(queryset, count_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'page_obj': page_obj,
    }
