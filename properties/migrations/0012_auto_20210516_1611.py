# Generated by Django 3.1.4 on 2021-05-16 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0011_auto_20210516_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='identifier_2',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]