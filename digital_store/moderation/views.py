from functools import wraps

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from core.actions import is_ajax
from core.pagination import get_context_paginator
from digital_store.settings import STAFF_ROLES
from users.models import User
from shop.models import Product, Shop

from .forms import RejectForm
from .models import AcceptRejectList


def get_last_page(request):
    return request.META.get('HTTP_REFERER')


def moderator_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role in STAFF_ROLES:
                return func(request, *args, **kwargs)
        return redirect('shop:index')
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                return func(request, *args, **kwargs)
        return redirect('shop:index')
    return wrapper


@moderator_required
def moderation_shop(request):
    """
    Страница модерации магазина
    """

    shops = Shop.objects.filter(status='In_Consideration')

    context = {
        'shops': shops,
    }

    context.update(get_context_paginator(shops, request))

    return render(
        request,
        context=context,
        template_name='moderation/shop_moderation.html',
    )


@require_POST
@moderator_required
def accept_shop(request, shop_id):
    """
    Обработка решения 'Принять' для магазина
    """

    shop = get_object_or_404(Shop, id=shop_id)
    shop.status = 'Accept'
    shop.save()

    if AcceptRejectList.objects.filter(shop=shop, product=None).exists():
        AcceptRejectList.objects.filter(shop=shop, product=None).update(
            type='shop',
            moderator=request.user,
            shop=shop,
            product=None,
            reason=None,
            update_date=timezone.now(),
        )
    else:
        AcceptRejectList.objects.create(
            type='shop',
            moderator=request.user,
            shop=shop,
            product=None,
            reason=None,
        )

    return redirect(get_last_page(request))


@moderator_required
def reject_shop(request, shop_id):
    """
    Обработка решения 'Отклонить' для магазина
    """

    form = RejectForm(request.POST or None)
    shop = get_object_or_404(Shop, id=shop_id)

    if form.is_valid():
        shop.status = 'Reject'
        shop.save()
        if AcceptRejectList.objects.filter(shop=shop, product=None).exists():
            AcceptRejectList.objects.filter(shop=shop, product=None).update(
                type='shop',
                moderator=request.user,
                shop=shop,
                product=None,
                reason=form.cleaned_data.get('reason'),
                update_date=timezone.now(),
            )
        else:
            AcceptRejectList.objects.create(
                type='shop',
                moderator=request.user,
                shop=shop,
                product=None,
                reason=form.cleaned_data.get('reason')
            )
        AcceptRejectList.objects.filter(shop=shop).exclude(
            product=None).update(
                reason='Статус магазина: Отклонено'
            )
        for product in shop.products.all():
            product.status = 'Reject'
            product.save()

        return redirect('moderation:moderation_history')

    context = {
        'shop': shop,
        'form': form,
    }

    return render(
        request,
        context=context,
        template_name='moderation/reject_reason.html',
    )


@moderator_required
def moderation_product(request):
    """
    Страница модерации продуктов
    """

    products = Product.objects.filter(status='In_Consideration')

    context = {
        'products': products,
    }

    context.update(get_context_paginator(products, request))

    return render(
        request,
        context=context,
        template_name='moderation/product_moderation.html',
    )


@require_POST
@moderator_required
def accept_product(request, product_id):
    """
    Обработка решения 'Принять' для продукта
    """

    product = get_object_or_404(Product, id=product_id)
    if product.shop.status == 'Reject':
        return redirect('shop:index')

    product.status = 'Accept'
    product.save()
    if AcceptRejectList.objects.filter(product=product).exists():
        AcceptRejectList.objects.filter(product=product).update(
            type='product',
            moderator=request.user,
            shop=product.shop,
            product=product,
            reason=None,
            update_date=timezone.now(),
        )
    else:
        AcceptRejectList.objects.create(
            type='product',
            moderator=request.user,
            shop=product.shop,
            product=product,
            reason=None,
        )
    return redirect('moderation:moderation_product')


@moderator_required
def reject_product(request, product_id):
    """
    Обработка решения 'Отклонить' для продукта
    """

    form = RejectForm(request.POST or None)
    product = get_object_or_404(Product, id=product_id)

    if form.is_valid():
        product.status = 'Reject'
        product.save()
        if AcceptRejectList.objects.filter(product=product).exists():
            AcceptRejectList.objects.filter(product=product).update(
                type='product',
                moderator=request.user,
                shop=product.shop,
                product=product,
                reason=form.cleaned_data.get('reason'),
                update_date=timezone.now(),
            )
        else:
            AcceptRejectList.objects.create(
                type='product',
                moderator=request.user,
                shop=product.shop,
                product=product,
                reason=form.cleaned_data.get('reason'),
            )
        return redirect('moderation:moderation_history')

    context = {
        'product': product,
        'form': form,
    }

    return render(
        request,
        context=context,
        template_name='moderation/reject_reason.html',
    )


@moderator_required
def moderation_history(request):
    """
    История действий модератора
    """

    history = (
        AcceptRejectList.objects
        .select_related('shop', 'product', 'moderator')
        .all().order_by('update_date')
    )

    context = {
        'history': history,
    }

    context.update(get_context_paginator(history, request))
    return render(
        request,
        context=context,
        template_name='moderation/moderation_history.html'
    )


@admin_required
def change_moderator_status(request):
    """
    Изменение статуса пользователя на модератора
    """

    if is_ajax(request=request) and request.method == 'POST':
        data = request.POST
        user = get_object_or_404(User, pk=data['user_id'])
        if user.role == 'moderator':
            user.role = 'user'
            user.save()
            is_moderator = False
        else:
            user.role = 'moderator'
            user.save()
            is_moderator = True

        context = {
            'is_moderator': is_moderator,
        }
        return JsonResponse(context, status=200)
    return JsonResponse({"success": False}, status=400)
