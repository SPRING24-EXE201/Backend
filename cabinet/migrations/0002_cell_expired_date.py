# Generated by Django 4.2.3 on 2024-01-11 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='expired_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
