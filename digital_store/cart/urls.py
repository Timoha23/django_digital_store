from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart,
         name='add_to_cart'),
    path('del_from_cart/<int:product_id>/', views.del_from_cart,
         name='del_from_cart'),
    path('make_order/', views.make_order, name='make_order'),
    path('add_count_items/', views.add_count_items,
         name='add_count_items'),
    path('remove_count_items/', views.remove_count_items,
         name='remove_count_items'),
    path('', views.cart, name='cart'),
]
