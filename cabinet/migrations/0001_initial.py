# Generated by Django 4.2.8 on 2023-12-26 14:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('start_using_date', models.CharField(max_length=100)),
                ('height', models.FloatField()),
                ('width', models.FloatField()),
                ('depth', models.FloatField()),
                ('status', models.BooleanField()),
                ('image_link', models.CharField(max_length=100)),
                ('virtual_cabinet_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CabinetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('status', models.BooleanField()),
                ('image_link', models.CharField(max_length=100)),
                ('cost_per_unit', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField(blank=True, default=None, null=True)),
                ('time_end', models.DateTimeField(blank=True, default=None, null=True)),
                ('status', models.BooleanField()),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('status', models.PositiveSmallIntegerField()),
                ('hash_code', models.CharField(max_length=100)),
                ('cell_index', models.PositiveSmallIntegerField()),
                ('width', models.FloatField()),
                ('height', models.FloatField()),
                ('depth', models.FloatField()),
                ('cabinet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.cabinet')),
            ],
        ),
        migrations.CreateModel(
            name='CostVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=100)),
                ('from_hour', models.FloatField()),
                ('to_hour', models.FloatField()),
                ('cost', models.FloatField()),
                ('unit', models.CharField(max_length=100)),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('kafka_id', models.CharField(max_length=100)),
                ('topic', models.CharField(max_length=100)),
                ('status', models.BooleanField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.location')),
            ],
        ),
        migrations.CreateModel(
            name='CellLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('status', models.BooleanField()),
                ('time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('cell_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.cell')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignCabinet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('cabinet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.cabinet')),
                ('campaign_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.campaign')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='cost_version_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.costversion'),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='cabinetType_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.cabinettype'),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='controller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.controller'),
        ),
    ]
