from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from shop.models import Product, User


class Review(models.Model):
    """
    Модель отзывов
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Пользователь',
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Продукт',
    )

    text = models.CharField(
        max_length=1024,
        verbose_name='Текст отзыва',
    )

    rating = models.PositiveIntegerField(
        default=5,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(5)
        ),
        verbose_name='Оценка',
    )

    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'От {self.user.username} отзыв для {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
