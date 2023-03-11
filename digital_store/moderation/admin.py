from django.contrib import admin

from .models import AcceptRejectList


class ModerationHistoryAdmin(admin.ModelAdmin):
    list_display = ('type', 'moderator', 'shop', 'product', 'reason',
                    'update_date', 'created_date')


admin.site.register(AcceptRejectList, ModerationHistoryAdmin)
