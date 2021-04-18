from django.db import models
from django.core.validators import RegexValidator
from accounts.models import CustomUser
from properties.validators import validate_file_size


class Realtor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], blank=True)
    country_code = models.CharField(max_length=6, blank=True)
    realtor_description = models.TextField(max_length=250, blank=True)
    realtor_logo = models.ImageField(upload_to='realtor_logos/%Y/%m/%d/', blank=True, validators=[validate_file_size])

    def __str__(self):
        
        return  f"{self.name} - {self.user.username}"