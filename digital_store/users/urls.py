from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('favorites/', views.get_favorite_list, name='favorites'),
    path('change_favorite/', views.change_favorite, name='change_favorite'),
    path('profile/<slug:username>/', views.user_profile, name='user_profile'),
    path('orders/', views.order_list, name='orders')
]
