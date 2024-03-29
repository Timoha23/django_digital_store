# Generated by Django 4.1.7 on 2023-03-11 09:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_alter_product_options_alter_shop_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0002_cart_updated_date_alter_cart_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, verbose_name='Полная цена')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата добавления в корзину')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('items', models.ManyToManyField(related_name='order_history', to='shop.item', verbose_name='Товары')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_history', to='shop.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_history', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='cart.orderhistory')),
            ],
        ),
    ]
