# Generated by Django 4.1.7 on 2023-03-08 09:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_product_visibile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='shop.product', verbose_name='Продукт'),
        ),
    ]
