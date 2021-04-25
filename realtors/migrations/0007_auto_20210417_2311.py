# Generated by Django 3.1.4 on 2021-04-17 23:11

from django.db import migrations, models
import properties.validators


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0006_auto_20210417_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtor',
            name='realtor_logo',
            field=models.ImageField(blank=True, upload_to='realtor_logos/%Y/%m/%d/', validators=[properties.validators.validate_file_size]),
        ),
    ]