from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLE = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=32,
        choices=USER_ROLE,
        default='user',
    )

    image = models.ImageField(
        default=None,
        upload_to='users/profile_img/',
        verbose_name='Изображение профиля',
        blank=True,
    )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
