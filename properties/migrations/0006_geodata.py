# Generated by Django 3.1.4 on 2021-05-13 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_auto_20210509_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='geoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_1', models.CharField(max_length=100)),
                ('admin_2', models.CharField(max_length=100)),
                ('admin_3', models.CharField(max_length=100)),
            ],
        ),
    ]
