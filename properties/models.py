from django.db import models
from accounts.models import CustomUser 
from datetime import datetime

class Properties(models.Model):
    FURNISHED = 'Furnished'
    UNFURNISHED = 'Unfurnished'
    FURNITURE_CHOICES = [
        (FURNISHED, 'Furnished'),
        (UNFURNISHED, 'Unfurnished'),
    ]
    realtor = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    property_type = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    postalcode = models.CharField(max_length=20)
    geo_lat = models.CharField(max_length=10)
    geo_lng = models.CharField(max_length=10)
    description = models.TextField(max_length=2000)
    short_description = models.TextField(max_length=150, default='')
    price = models.IntegerField()
    bedrooms = models.DecimalField(max_digits=2, decimal_places=0)
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    furniture = models.CharField(max_length=11,choices=FURNITURE_CHOICES, default=FURNISHED)
    m2 = models.IntegerField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    for_sale = models.BooleanField(default=False)
    to_rent = models.BooleanField(default=False)
    list_date = models.DateTimeField(default=datetime.now, blank=True)  
    
    def __str__(self):
        
        return self.address
