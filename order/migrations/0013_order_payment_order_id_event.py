# Generated by Django 4.2.3 on 2024-02-26 08:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_assignment_delete_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_order_id',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('dataId', models.CharField(blank=True, max_length=100, null=True)),
                ('timestamp', models.DateTimeField()),
                ('eventType', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('data', models.CharField(blank=True, max_length=10000, null=True)),
                ('orderDetail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderdetail')),
            ],
        ),
    ]