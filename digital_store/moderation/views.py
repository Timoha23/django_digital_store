from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404

from digital_store.settings import STAFF_ROLES
from shop.models import Shop, Product
from .models import ModerationHistory
from .forms import RejectForm


def moderator_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role in STAFF_ROLES:
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

    return render(
        request,
        context=context,
        template_name='moderation/shop_moderation.html',
    )


@moderator_required
def accept_shop(request, shop_id):
    """
    Обработка решения 'Принять' для магазина
    """

    shop = get_object_or_404(Shop, id=shop_id)
    shop.status = 'Accept'
    shop.save()

    if ModerationHistory.objects.filter(shop=shop).exists():
        ModerationHistory.objects.filter(shop=shop).update(
            type='shop',
            moderator=request.user,
            shop=shop,
            product=None,
            reason=None,
        )
    else:
        ModerationHistory.objects.create(
            type='shop',
            moderator=request.user,
            shop=shop,
            product=None,
            reason=None,
        )

    return redirect('moderation:moderation_shop')


@moderator_required
def reject_shop(request, shop_id):
    """
    Обработка решения 'Отклонить' для магазина
    """

    form = RejectForm(request.POST or None)
    shop = get_object_or_404(Shop, id=shop_id)
    print(shop)
    if form.is_valid():
        shop.status = 'Reject'
        shop.save()
        if ModerationHistory.objects.filter(shop=shop).exists():
            ModerationHistory.objects.filter(shop=shop).update(
                type='shop',
                moderator=request.user,
                shop=shop,
                product=None,
                reason=form.cleaned_data.get('reason')
            )
        else:
            ModerationHistory.objects.create(
                type='shop',
                moderator=request.user,
                shop=shop,
                product=None,
                reason=form.cleaned_data.get('reason')
            )
        return redirect('moderation:moderation_shop')

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

    return render(
        request,
        context=context,
        template_name='moderation/product_moderation.html',
    )


@moderator_required
def accept_product(request, product_id):
    """
    Обработка решения 'Принять' для продукта
    """

    product = get_object_or_404(Product, id=product_id)
    product.status = 'Accept'
    product.save()
    if ModerationHistory.objects.filter(product=product).exists():
        ModerationHistory.objects.filter(product=product).update(
            type='product',
            moderator=request.user,
            shop=product.shop,
            product=product,
            reason=None,
        )
    else:
        ModerationHistory.objects.create(
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
        if ModerationHistory.objects.filter(product=product).exists():
            ModerationHistory.objects.filter(product=product).update(
                type='product',
                moderator=request.user,
                shop=product.shop,
                product=product,
                reason=form.cleaned_data.get('reason')
            )
        else:
            ModerationHistory.objects.create(
                type='product',
                moderator=request.user,
                shop=product.shop,
                product=product,
                reason=None,
            )
        return redirect('moderation:moderation_product')

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

    history = ModerationHistory.objects.select_related('shop').select_related('product').select_related('moderator').all()

    context = {
        'history': history,
    }
    print(history)
    return render(
        request,
        context=context,
        template_name='moderation/moderation_history.html'
    )
