from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator
from accounts.models import CustomUser
from properties.validators import validate_file_size


class Organisation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], blank=True)
    country_code = models.CharField(max_length=6, blank=True)
    organisation_description = models.TextField(max_length=250, blank=True)
    organisation_logo = models.ImageField(upload_to='organisation_logos/%Y/%m/%d/', blank=True, validators=[validate_file_size])

    def __str__(self):
        
        return  self.name
    
class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    active_agent = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True) 
    
    def __str__(self):
        return self.user.username