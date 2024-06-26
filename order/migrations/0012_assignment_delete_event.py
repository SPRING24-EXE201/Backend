# Generated by Django 4.2.3 on 2024-02-05 14:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100)),
                ('status', models.BooleanField()),
                ('orderDetail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderdetail')),
            ],
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
