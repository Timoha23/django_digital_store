from django.urls import path

from . import views

app_name = 'review'

urlpatterns = [
    path('add/product/<int:product_id>/', views.review_add, name='review_add'),
    path('shop/<int:shop_id>/', views.reviews_shop_list,
         name='reviews_shop_list'),
]
