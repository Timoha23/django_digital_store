from django.db import models
from django.contrib.auth.models import AbstractUser

# from shop.models import Product


class User(AbstractUser):
    USER_ROLE = (
        ('user', 'Пользователь'),
        ('seller', 'Продавец'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=32,
        choices=USER_ROLE,
        default='user',
    )

    @property
    def is_seller(self):
        return self.role == 'seller'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username


class Favorite(models.Model):
    """
    Модель избранного
    """

    user = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    product = models.ForeignKey(
        'shop.Product',
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    def __str__(self):
        return f'{self.user} <3 {self.product}'

    class Meta:
        constraints = [models.UniqueConstraint(fields=('user', 'product'),
                       name='Уникальные значения')]
