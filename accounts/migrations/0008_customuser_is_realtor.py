# Generated by Django 3.1.4 on 2021-04-16 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_delete_globalmapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_realtor',
            field=models.BooleanField(default=False),
        ),
    ]
