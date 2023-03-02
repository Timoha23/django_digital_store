from django.urls import path

from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/<slug:shop_name>/', views.shop, name='shop'),
    path('item/<int:item_id>/', views.item, name='item')
]
