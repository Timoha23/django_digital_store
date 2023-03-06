from django.contrib import admin

from .models import ModerationHistory


class ModerationHistoryAdmin(admin.ModelAdmin):
    list_display = ('type', 'moderator', 'shop', 'product', 'reason',
                    'update_date', 'created_date')


admin.site.register(ModerationHistory, ModerationHistoryAdmin)
