# Generated by Django 4.1.7 on 2023-03-05 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_status_shop_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='image',
            field=models.ImageField(blank=True, upload_to='shop', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='Название'),
        ),
    ]