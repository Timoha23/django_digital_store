from django.urls import path

from . import views


app_name = 'shop'

urlpatterns = [
    path('shop/<int:shop_id>/', views.shop, name='shop'),
    path('product/<int:item_id>/', views.product, name='product'),
    path('create_shop/', views.create_shop, name='create_shop'),
    path('edit_shop/<int:shop_id>/', views.edit_shop, name='edit_shop'),
    path('delete_shop/<int:shop_id>/', views.delete_shop, name='delete_shop'),
    path('user_shops/', views.user_shops, name='user_shops'),
    path('cart/', views.cart, name='user_cart'),
    path('', views.index, name='index'),
]
