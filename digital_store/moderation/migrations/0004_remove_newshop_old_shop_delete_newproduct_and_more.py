# Generated by Django 4.1.7 on 2023-03-06 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0003_remove_newproduct_new_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newshop',
            name='old_shop',
        ),
        migrations.DeleteModel(
            name='NewProduct',
        ),
        migrations.DeleteModel(
            name='NewShop',
        ),
    ]
