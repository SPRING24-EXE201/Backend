# Generated by Django 4.2.3 on 2024-01-21 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0006_alter_costversion_to_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaigncabinet',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign', to='cabinet.campaign'),
        ),
    ]
