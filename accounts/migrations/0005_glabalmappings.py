# Generated by Django 3.1.4 on 2021-03-26 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_customuser_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlabalMappings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mappingGroup', models.CharField(max_length=200)),
                ('mappingType', models.CharField(max_length=200)),
                ('mappingFromValue', models.CharField(max_length=200)),
                ('mappingToValue', models.CharField(max_length=200)),
            ],
        ),
    ]
