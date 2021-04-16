from django.db import models
from django.core.validators import RegexValidator
from accounts.models import CustomUser


class Realtor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    country_code = models.CharField(max_length=6)

    def __str__(self):
        return self.name