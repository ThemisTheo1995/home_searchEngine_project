# Generated by Django 3.2.5 on 2021-08-27 09:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('properties', '0027_properties_saved_property'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='properties',
            name='saved_property',
        ),
        migrations.AddField(
            model_name='properties',
            name='favourite',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='list of saved properties'),
        ),
    ]
