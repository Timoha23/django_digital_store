from django.contrib import admin

from .models import Favorite, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('username',)
    list_filter = ('role',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_date')
    search_fields = ('user__username', 'product__name')


admin.site.register(User, UserAdmin)
admin.site.register(Favorite, FavoriteAdmin)

