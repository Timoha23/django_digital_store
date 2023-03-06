from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Shop, Product
from .models import ModerationHistory
from .forms import RejectForm


def shop_moderation(request):
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


def accept_shop(request, shop_id):
    """
    Обработка решения 'Принять' для магазина
    """

    shop = get_object_or_404(Shop, id=shop_id)
    shop.status = 'Accept'
    shop.save()

    ModerationHistory.objects.create(
        type='shop',
        moderator=request.user,
        shop=shop,
        product=None,
        reason=None,
    )
    return redirect('moderation:shop_moderation')


def reject_shop(request, shop_id):
    """
    Обработка решения 'Отклонить' для магазина
    """

    form = RejectForm(request.POST or None)
    shop = get_object_or_404(Shop, id=shop_id)

    if form.is_valid():
        shop.status = 'Reject'
        shop.save()
        ModerationHistory.objects.create(
            type='shop',
            moderator=request.user,
            shop=shop,
            product=None,
            reason=form.cleaned_data.get('reason')
        )
        return redirect('moderation:shop_moderation')

    context = {
        'shop': shop,
        'form': form,
    }

    return render(
        request,
        context=context,
        template_name='moderation/reject_reason.html',
    )


def product_moderation(request):
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


def accept_product(request, product_id):
    """
    Обработка решения 'Принять' для продукта
    """

    product = get_object_or_404(Product, id=product_id)
    product.status = 'Accept'
    product.save()

    ModerationHistory.objects.create(
        type='product',
        moderator=request.user,
        shop=product.shop,
        product=product,
        reason=None,
    )
    return redirect('moderation:product_moderation')


def reject_product(request, product_id):
    """
    Обработка решения 'Отклонить' для продукта
    """

    form = RejectForm(request.POST or None)
    product = get_object_or_404(Product, id=product_id)

    if form.is_valid():
        product.status = 'Reject'
        product.save()
        ModerationHistory.objects.create(
            type='product',
            moderator=request.user,
            shop=product.shop,
            product=product,
            reason=form.cleaned_data.get('reason')
        )
        return redirect('moderation:product_moderation')

    context = {
        'product': product,
        'form': form,
    }

    return render(
        request,
        context=context,
        template_name='moderation/reject_reason.html',
    )
