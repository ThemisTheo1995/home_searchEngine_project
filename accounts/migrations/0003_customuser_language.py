# Generated by Django 3.1.4 on 2021-03-26 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210307_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='language',
            field=models.CharField(choices=[('English', 'English'), ('Greek', 'Ελληνικά')], default='English', max_length=100),
        ),
    ]