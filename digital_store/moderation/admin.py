from django.contrib import admin

from .models import AcceptRejectList


class ModerationHistoryAdmin(admin.ModelAdmin):
    list_display = ('type', 'moderator', 'shop', 'product', 'get_status',
                    'reason', 'update_date', 'created_date')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('shop', 'product', 'moderator')

    def get_status(self, obj):
        if obj.type == 'shop':
            return obj.shop.get_status_display()
        return obj.product.get_status_display()

    get_status.short_description = 'Статус'


admin.site.register(AcceptRejectList, ModerationHistoryAdmin)
