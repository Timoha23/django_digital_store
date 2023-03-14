from django.contrib import admin

from .models import User, Favorite


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


admin.site.register(User, UserAdmin)
admin.site.register(Favorite, FavoriteAdmin)
