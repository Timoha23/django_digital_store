from django.contrib import admin

from .models import Cart, Order, OrderHistory


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'get_price', 'get_full_price',
                    'count_items', 'updated_date')

    def get_price(self, obj):
        return None

    def get_full_price(self, obj):
        return None


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_date',)


class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'product', 'get_items',
                    'price', 'full_price', 'count_items')

    def get_items(self, obj):
        return "\n".join([c.item for c in obj.items.all()])


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
