# Generated by Django 4.1.7 on 2023-03-11 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cart_items_orderhistory_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order',
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order_history', to='cart.order'),
            preserve_default=False,
        ),
    ]
