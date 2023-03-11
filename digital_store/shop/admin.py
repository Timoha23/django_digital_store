from django.contrib import admin

from .models import Shop, Product, Item, Category


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'image', 'description',
                    'created_date')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'shop', 'get_categories', 'get_items',
                    'description', 'count', 'visibile', 'created_date')

    def get_categories(self, obj):
        return "\n".join([c.name for c in obj.category.all()])

    def get_items(self, obj):
        return "\n".join([c.item for c in obj.item.all() if c.status=='sale'])


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'item', 'status', 'created_date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_date')


admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
