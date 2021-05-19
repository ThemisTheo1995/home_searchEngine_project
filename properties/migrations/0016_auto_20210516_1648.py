# Generated by Django 3.1.4 on 2021-05-16 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0015_auto_20210516_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geodata',
            name='admin_1',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_1_en',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_2',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_2_en',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_3',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_3_en',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_4',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='admin_4_en',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='country_en',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='geodata',
            name='identifier',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
