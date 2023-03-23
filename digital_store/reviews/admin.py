from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'rating',
                    'update_date', 'created_date')
    search_fields = ('user__username', 'product__name')
    list_filter = ('rating',)


admin.site.register(Review, ReviewAdmin)
