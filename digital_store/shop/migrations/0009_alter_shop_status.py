# Generated by Django 4.1.7 on 2023-03-06 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_product_price_alter_item_product_alter_product_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='status',
            field=models.CharField(choices=[('Accept', 'Одобрено'), ('Reject', 'Отклонено'), ('In_Consideration', 'В рассмотрении')], default='In_Consideration', max_length=32),
        ),
    ]
