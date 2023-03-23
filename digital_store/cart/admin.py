from django.contrib import admin

from .models import Cart, Order, OrderHistory


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'get_price', 'get_full_price',
                    'count_items', 'updated_date', 'created_date',)
    search_fields = ('user__username', 'product__name')
    list_filter = ('created_date',)

    def get_price(self, obj):
        return obj.product.price

    def get_full_price(self, obj):
        return obj.product.price * obj.count_items

    get_price.short_description = 'Цена за единицу'
    get_full_price.short_description = 'Полная цена'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_user', 'get_products', 'created_date',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return (
            queryset.prefetch_related('order_history__product')
                    .prefetch_related('order_history__user')
        )

    def get_user(self, obj):
        return obj.order_history.all()[0].user

    def get_products(self, obj):
        return " | ".join([pr.product.name for pr in obj.order_history.all()])

    get_user.short_description = 'Пользователь'
    get_products.short_description = 'Продукты'


class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'product', 'get_items',
                    'price', 'full_price', 'count_items', 'review',
                    'created_date')
    search_fields = ('user__username', 'order__pk',)
    list_filter = ('created_date',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('items', 'product')

    def get_items(self, obj):
        return " | ".join([c.item for c in obj.items.all()])


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
