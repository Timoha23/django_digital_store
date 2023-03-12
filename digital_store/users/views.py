from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cart.models import Order
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('shop:index')
    template_name = 'users/signup.html'


def user_profile(request, username):
    """
    Профиль пользователя
    """
    print(username)
    return render(request, template_name='users/profile.html')


@login_required
def order_list(request):
    """
    Отображение списка покупок для юзера
    """

    orders = (Order.objects.filter(order_history__user=request.user)
              .distinct().prefetch_related('order_history__product__shop')
              .order_by('-created_date')
              )

    for o in orders:
        print(o.order_history.all())

    context = {
        'orders': orders,
    }
    return render(request, context=context, template_name='users/orders.html')
