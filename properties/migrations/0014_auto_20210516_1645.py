# Generated by Django 3.1.4 on 2021-05-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0013_auto_20210516_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geodata',
            name='identifier',
            field=models.CharField(blank=True, default=0, max_length=100),
        ),
    ]
