from django.contrib import admin

from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'get_items', 'price', 'full_price',
                    'count_items', 'updated_date')

    def get_items(self, obj):
        return "\n".join([c.item for c in obj.items.all()])


admin.site.register(Cart, CartAdmin)
