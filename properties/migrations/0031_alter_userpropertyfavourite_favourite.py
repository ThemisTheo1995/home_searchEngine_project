# Generated by Django 3.2.5 on 2021-10-26 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0030_remove_properties_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpropertyfavourite',
            name='favourite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='properties.properties'),
        ),
    ]
