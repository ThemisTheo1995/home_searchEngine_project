# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from properties.validators import validate_file_size
from django.utils.translation import ugettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_realtor = models.BooleanField(default=False, verbose_name=_('Signed up as realtor?'))
    is_agent = models.BooleanField(default=False, verbose_name=_('Signed up as agent?'))
    profile_picture = models.ImageField(upload_to='profile_picture/%Y/%m/%d/', blank=True, validators=[validate_file_size], verbose_name=_('Profile picture'))
    
    
    def __str__(self):
        return self.username
