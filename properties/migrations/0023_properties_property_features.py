# Generated by Django 3.1.4 on 2021-05-25 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0022_auto_20210524_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='property_features',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]
