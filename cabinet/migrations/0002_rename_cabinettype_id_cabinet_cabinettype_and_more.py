# Generated by Django 4.2.3 on 2024-01-19 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cabinet',
            old_name='cabinetType_id',
            new_name='CabinetType',
        ),
        migrations.RenameField(
            model_name='cabinet',
            old_name='controller_id',
            new_name='Controller',
        ),
        migrations.RenameField(
            model_name='campaign',
            old_name='cost_version_id',
            new_name='CostVersion',
        ),
        migrations.RenameField(
            model_name='campaigncabinet',
            old_name='cabinet_id',
            new_name='Cabinet',
        ),
        migrations.RenameField(
            model_name='campaigncabinet',
            old_name='campaign_id',
            new_name='Campaign',
        ),
        migrations.RenameField(
            model_name='cell',
            old_name='cabinet_id',
            new_name='Cabinet',
        ),
        migrations.RenameField(
            model_name='celllog',
            old_name='cell_id',
            new_name='Cell',
        ),
        migrations.RenameField(
            model_name='controller',
            old_name='location_id',
            new_name='Location',
        ),
    ]
