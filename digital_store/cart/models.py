from django.db import models

from shop.models import Product, Item
from users.models import User


class Cart(models.Model):
    """
    Модель корзины
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart',
    )

    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Продукт',
        related_name='cart',
    )

    items = models.ManyToManyField(
        Item,
        verbose_name='Товары',
        related_name='cart',
    )

    price = models.FloatField(
        default=0,
        verbose_name='Цена за единицу товара',
    )

    full_price = models.FloatField(
        default=0,
        verbose_name='Полная цена',
    )

    count_items = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )

    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата добавления в корзину',
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания заказа',
    )

    def __str__(self):
        return f'{self.user.username} купил {self.product.name}'
