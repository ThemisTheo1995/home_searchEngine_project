# Generated by Django 3.1.4 on 2021-06-19 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0024_auto_20210606_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='properties',
            name='street_number',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
