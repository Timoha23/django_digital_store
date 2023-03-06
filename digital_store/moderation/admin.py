from django.contrib import admin

from .models import ModerationHistory


class ModerationHistoryAdmin(admin.ModelAdmin):
    fields = ('type', 'moderator', 'shop', 'product', 'reason',
              'created_date')


admin.site.register(ModerationHistory, ModerationHistoryAdmin)
