# Generated by Django 4.2.3 on 2024-01-19 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0003_alter_cell_hash_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='cost_version_id',
        ),
        migrations.AddField(
            model_name='campaign',
            name='cost_version',
            field=models.CharField(default='UNUSABLE', max_length=100),
        ),
    ]
