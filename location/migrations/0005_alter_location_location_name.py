# Generated by Django 4.2.3 on 2024-01-19 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_location_location_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
