# Generated by Django 3.1.4 on 2021-06-06 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0023_properties_property_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='short_description',
            field=models.TextField(default='', max_length=230),
        ),
    ]
