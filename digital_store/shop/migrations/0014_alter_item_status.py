# Generated by Django 4.1.7 on 2023-03-08 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('in_cart', 'В корзине'), ('sold', 'Продан'), ('sale', 'Продается')], default='sale', max_length=32, verbose_name='Статус товара'),
        ),
    ]
