# Generated by Django 4.1.7 on 2023-03-05 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_shop_image_alter_shop_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='image',
            field=models.ImageField(blank=True, default='/static/img/default/shop.jpg', upload_to='shop', verbose_name='Изображение'),
        ),
    ]