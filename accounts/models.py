from django.contrib.auth.models import AbstractUser
from django.db import models
from properties.validators import validate_file_size

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_realtor = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_picture/%Y/%m/%d/', blank=True, validators=[validate_file_size])
    
    
    def __str__(self):
        return self.username
