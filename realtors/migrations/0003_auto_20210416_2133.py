# Generated by Django 3.1.4 on 2021-04-16 21:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0002_auto_20210416_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtor',
            name='country_code',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='phone',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
    ]