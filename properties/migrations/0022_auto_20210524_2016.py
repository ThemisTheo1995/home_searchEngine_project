# Generated by Django 3.1.4 on 2021-05-24 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0021_auto_20210523_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='property_type',
            field=models.CharField(choices=[('Flat/Apartment', 'Flat/Apartment'), ('Cottage', 'Cottage'), ('Detached', 'Detached'), ('Semi-Detached', 'Semi-Detached'), ('Terraced', 'Terraced'), ('Studio', 'Studio'), ('Bungalow', 'Bungalow'), ('Penthouse', 'Penthouse'), ('Land', 'Land'), ('Shared', 'Shared')], default='Flat/Apartment', max_length=100),
        ),
    ]
