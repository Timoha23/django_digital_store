from django.db import models

from shop.models import Shop, Product
from users.models import User


class ModerationHistory(models.Model):
    TYPE_MODERATION = (
        ('shop', 'Магазин'),
        ('product', 'Продукт'),
    )
    type = models.CharField(
        max_length=16,
        choices=TYPE_MODERATION,
        verbose_name='Тип',
    )
    moderator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='moderator_in_moderation_history',
        verbose_name='Модератор',
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='shop_in_moderation_history',
        verbose_name='Магазин',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='product_in_moderation_history',
        verbose_name='Продукт',
        null=True,
        default=None,
    )
    reason = models.CharField(
        max_length=512,
        verbose_name='Причина',
        null=True,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата проверки',
    )

    def __str__(self):
        return self.type
