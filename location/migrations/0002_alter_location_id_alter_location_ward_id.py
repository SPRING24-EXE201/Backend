# Generated by Django 4.2.3 on 2024-01-11 00:57

from django.db import migrations, models
import django.db.models.deletion
import utils.custom_id


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='id',
            field=models.CharField(default=utils.custom_id.location_custom_id, editable=False, max_length=17, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='ward_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.ward'),
        ),
    ]