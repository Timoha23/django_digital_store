# Generated by Django 4.1.7 on 2023-03-11 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_shop_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created_date',)},
        ),
    ]
