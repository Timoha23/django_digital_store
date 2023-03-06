from django.db import models

from users.models import User

PRODUCT_AND_SHOP_STATUS = (
        ('Accept', 'Одобрено'),
        ('Reject', 'Отклонено'),
        ('In_Consideration', 'В рассмотрении'),
    )

DEFAULT_STATUS = PRODUCT_AND_SHOP_STATUS[-1][0]


class Shop(models.Model):
    """
    Модель магазина
    """

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
        choices=PRODUCT_AND_SHOP_STATUS,
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

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель продукта
    """

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
        related_name='shop_in_product',
        verbose_name='Магазин',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    category = models.ManyToManyField(
        Category,
        related_name='category',
        # default=get_default_category(),
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to='shop/product/',
        verbose_name='Изображение',
        blank=True,
    )
    description = models.CharField(
        max_length=1024,
        verbose_name='Описание',
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество товара'
    )
    visibile = models.BooleanField(
        default=True,
        verbose_name='Видимость продукта',
    )
    status = models.CharField(
        max_length=32,
        choices=PRODUCT_AND_SHOP_STATUS,
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
        related_name='product_in_item',
        verbose_name='Продукт',
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
