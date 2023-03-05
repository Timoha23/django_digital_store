from django.db import models
from django.templatetags.static import static

from users.models import User


class Shop(models.Model):
    """
    Модель магазина
    """

    SHOP_STATUS = (
        ('Reject', 'Reject'),
        ('Accept', 'Accept'),
        ('In_Consideration', 'В рассмотрении'),
    )
    DEFAULT_STATUS = SHOP_STATUS[-1][0]

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='owner',
    )
    image = models.ImageField(
        upload_to='shop',
        verbose_name='Изображение',
        blank=True,
    )
    description = models.CharField(
        max_length=1028,
        verbose_name='Описание',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    status = models.CharField(
        max_length=32,
        choices=SHOP_STATUS,
        default=DEFAULT_STATUS,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель категорий товаров
    """

    name = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )


class Product(models.Model):
    """
    Модель продукта
    """

    PRODUCT_STATUS = (
        ('Reject', 'Отклонено'),
        ('Accept', 'Принято'),
        ('In_Consideration', 'В рассмотрении'),
    )
    DEFAULT_STATUS = PRODUCT_STATUS[-1][0]
    # @staticmethod
    # def get_default_category():
    #     default_category = Category.objects.get(name='default')
    #     return default_category

    name = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='shop',
        verbose_name='Магазин',
    )
    category = models.ManyToManyField(
        Category,
        related_name='category',
        # default=get_default_category(),
        verbose_name='Категория',
    )
    description = models.CharField(
        max_length=1024,
        verbose_name='Описание',
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество товара'
    )
    visibile = models.BooleanField(
        default=False,
        verbose_name='Видимость продукта',
    )
    status = models.CharField(
        max_length=32,
        choices=PRODUCT_STATUS,
        default=DEFAULT_STATUS,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Модель отдельного товара в продукте
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    item = models.CharField(
        max_length=1024,
        verbose_name='Товар',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )


class BrowsingHistory(models.Model):
    """
    Модель истории просмотра товара юзером
    """
    ...
