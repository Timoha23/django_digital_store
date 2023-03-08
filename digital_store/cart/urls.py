from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    path('add_to_cart/product/<int:product_id>/', views.add_to_cart, name='add_to_cart')
]
