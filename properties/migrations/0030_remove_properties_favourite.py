# Generated by Django 3.2.5 on 2021-08-27 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0029_userpropertyfavourite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='properties',
            name='favourite',
        ),
    ]