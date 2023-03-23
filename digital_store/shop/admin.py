from django.contrib import admin

from .models import Shop, Product, Item, Category


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'image', 'description',
                    'status', 'created_date')
    search_fields = ('name', 'owner__username')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'shop', 'get_categories', 'get_items',
                    'description', 'count', 'visibile', 'created_date')
    search_fields = ('name', 'shop__name')
    list_filter = ('visibile',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('category', 'item')

    def get_categories(self, obj):
        return "\n".join([c.name for c in obj.category.all()])

    def get_items(self, obj):
        return "\n".join([c.item for c in obj.item.all()
                          if c.status == 'sale'])

    get_categories.short_description = 'Категории'
    get_items.short_description = 'Товары'


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'get_shop', 'item', 'status',
                    'created_date')
    search_fields = ('product__name', 'product__shop__name')
    list_filter = ('status',)

    def get_shop(self, obj):
        return obj.product.shop

    get_shop.short_description = 'Магазин'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'created_date')
    search_fields = ('name', 'slug')


admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
