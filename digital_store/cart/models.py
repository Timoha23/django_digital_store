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
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='cart',
    )

    count_items = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )

    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования',
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата внесения в корзину',
    )


class Order(models.Model):

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания заказа',
    )

    def __str__(self):
        return str(self.pk)


class OrderHistory(models.Model):
    """
    Модель истории заказов для каждого продукта
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='order_history',
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_history',
    )

    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Продукт',
        related_name='order_history',
    )

    items = models.ManyToManyField(
        Item,
        verbose_name='Товары',
        related_name='order_history',
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

    review = models.BooleanField(
        default=False,
        verbose_name='Отзыв оставлен',
    )

    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования',
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания заказа',
    )
