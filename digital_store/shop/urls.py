from django.urls import path

from . import views


app_name = 'shop'

urlpatterns = [
    path('shop/<int:shop_id>/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('create_shop/', views.create_shop, name='create_shop'),
    path('edit_shop/<int:shop_id>/', views.edit_shop, name='edit_shop'),
    path('delete_shop/<int:shop_id>/', views.delete_shop, name='delete_shop'),
    path('shop/<int:shop_id>/create_product/', views.create_product,
         name='create_product'),
    path('shop/<int:shop_id>/edit_product/<int:product_id>/',
         views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product,
         name='delete_product'),
    path('product/<int:product_id>/create_item/', views.create_item,
         name='create_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('user_shops/', views.user_shops, name='user_shops'),
    path('cart/', views.cart, name='user_cart'),
    path('shops/', views.shop_list, name='shop_list'),
    path('products/', views.product_list, name='product_list'),
    path('', views.index, name='index'),
]
