# Generated by Django 4.2.8 on 2023-12-26 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100)),
                ('code_name', models.CharField(max_length=100)),
                ('code_name_en', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AdministrativeUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=100)),
                ('full_name_en', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=100)),
                ('short_name_en', models.CharField(max_length=100)),
                ('code_name', models.CharField(max_length=100)),
                ('code_name_en', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=100)),
                ('full_name_en', models.CharField(max_length=100)),
                ('code_name', models.CharField(max_length=100)),
                ('administrative_unit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.administrativeunit')),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=100)),
                ('full_name_en', models.CharField(max_length=100)),
                ('code_name', models.CharField(max_length=100)),
                ('administrative_unit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.administrativeunit')),
                ('district_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.district')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=100)),
                ('full_name_en', models.CharField(max_length=100)),
                ('code_name', models.CharField(max_length=100)),
                ('administrative_region_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.administrativeregion')),
                ('administrative_unit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.administrativeunit')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_detail', models.CharField(max_length=100)),
                ('ward_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.ward')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='province_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.province'),
        ),
    ]