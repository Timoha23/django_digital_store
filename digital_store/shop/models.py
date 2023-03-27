from django.db import models

from cart.models import Cart
from users.models import User, Favorite

PRODUCT_AND_SHOP_STATUS = (
        ('Accept', 'Одобрено'),
        ('Reject', 'Отклонено'),
        ('In_Consideration', 'В рассмотрении'),
    )

DEFAULT_STATUS = PRODUCT_AND_SHOP_STATUS[-1][0]

ITEM_STATUS = (
    ('in_cart', 'В корзине'),
    ('sold', 'Продан'),
    ('sale', 'Продается')
)


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
        default=None,
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

    def save(self, *args, **kwargs):
        Cart.objects.filter(product__shop=self).delete()
        Favorite.objects.filter(product__shop=self).delete()
        super(Shop, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class Category(models.Model):
    """
    Модель категорий товаров
    """

    name = models.CharField(
        max_length=128,
        verbose_name='Название',
    )

    slug = models.SlugField(
        unique=True,
        max_length=20,
        verbose_name='Уникальный адрес категории',
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """
    Модель продукта
    """

    name = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Магазин',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    category = models.ManyToManyField(
        Category,
        blank=True,
        related_name='category',
        verbose_name='Категория',
    )
    image = models.ImageField(
        default=None,
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
    is_available = models.BooleanField(
        default=False,
        verbose_name='В наличии'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    def save(self, *args, **kwargs):
        if self.count > 0:
            self.is_available = True
        else:
            self.is_available = False
        Cart.objects.filter(product=self).delete()
        Favorite.objects.filter(product=self).delete()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Item(models.Model):
    """
    Модель отдельного товара в продукте
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='item',
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

    status = models.CharField(
        default='sale',
        max_length=32,
        choices=ITEM_STATUS,
        verbose_name='Статус товара',
    )

    def __str__(self):
        return self.item

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
