# Generated by Django 3.1.4 on 2021-05-20 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0018_auto_20210520_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geodata',
            name='admin_1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_1_en',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_2_en',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_3',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_3_en',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_4',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_4_en',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='country_en',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='identifier',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='location',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='location_en',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
