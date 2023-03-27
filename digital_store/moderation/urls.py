from django.urls import path

from . import views

app_name = 'moderation'

urlpatterns = [
     path('shops/', views.moderation_shop, name='moderation_shop'),
     path('accept_shop/<int:shop_id>/', views.accept_shop, name='accept_shop'),
     path('reject_shop/<int:shop_id>/', views.reject_shop, name='reject_shop'),
     path('products/', views.moderation_product, name='moderation_product'),
     path('accept_product/<int:product_id>/', views.accept_product,
          name='accept_product'),
     path('reject_product/<int:product_id>/', views.reject_product,
          name='reject_product'),
     path('moderation_history/', views.moderation_history,
          name='moderation_history'),
]
