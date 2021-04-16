from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_realtor = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


