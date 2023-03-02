from django.db import models
from django.contrib.auth.models import AbstractUser


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
