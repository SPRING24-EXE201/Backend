# Generated by Django 4.2.3 on 2024-02-26 09:04

from django.db import migrations, models
import exe201_backend.common.custom_id


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_order_payment_order_id_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_order_id',
            field=models.IntegerField(default=exe201_backend.common.custom_id.payment_order_id, unique=True),
        ),
    ]
