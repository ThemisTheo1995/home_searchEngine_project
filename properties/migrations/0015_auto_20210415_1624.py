# Generated by Django 3.1.4 on 2021-04-15 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0014_auto_20210415_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='property_category',
            field=models.CharField(choices=[('FEATURED', 'FEATURED'), ('OPPORTUNITY', 'OPPORTUNITY'), ('STANDARD', 'STANDARD')], default='', max_length=25),
        ),
    ]