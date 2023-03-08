# Generated by Django 4.1.7 on 2023-03-08 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата добавления в корзину'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа'),
        ),
    ]
