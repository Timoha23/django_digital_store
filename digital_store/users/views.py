from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render

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
