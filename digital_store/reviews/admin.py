from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'product', 'text', 'rating',
                    'update_date', 'created_date')


admin.site.register(Review, ReviewAdmin)
