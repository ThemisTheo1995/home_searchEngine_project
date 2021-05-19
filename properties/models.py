from django.db import models
from accounts.models import CustomUser 
from datetime import datetime
from .validators import validate_file_size, validate_postcode
from realtors.models import Organisation,Agent

class geoData(models.Model):
    country = models.CharField(max_length=100, blank=True, default='')
    country_en = models.CharField(max_length=100, blank=True, default='')
    admin_1 = models.CharField(max_length=100, blank=True, default='')
    admin_1_en = models.CharField(max_length=100, blank=True, default='')
    admin_2 = models.CharField(max_length=100, blank=True, default='')
    admin_2_en = models.CharField(max_length=100, blank=True, default='')
    admin_3 = models.CharField(max_length=100, blank=True, default='')
    admin_3_en = models.CharField(max_length=100, blank=True, default='')
    admin_4 = models.CharField(max_length=100, blank=True, default='')
    admin_4_en = models.CharField(max_length=100, blank=True, default='')
    identifier = models.CharField(max_length=100, blank=True, default='')
    def __str__(self):
        return f"{self.admin_1}, {self.admin_2}, {self.admin_3}"

class geoSearch(models.Model):
    location = models.CharField(max_length=150)
    identifier = models.CharField(max_length=12)
    def __str__(self):
        return f"{self.location}, {self.identifier}"

class Properties(models.Model):
    FURNITURE_CHOICES = [
        ('Furnished', 'Furnished'),
        ('Unfurnished', 'Unfurnished'),
    ]
    CURRENCY_CHOICES = [
        ('€', 'EUR(€)'),
        ('£', 'GBP(£)'),
        ('$', 'USD($)'),
    ]
    PROPERTY_CATEGORY_CHOICES = [
        ('FEATURED', 'FEATURED'),
        ('OPPORTUNITY', 'OPPORTUNITY'),
        ('STANDARD', 'STANDARD'),        
    ]
    ADVERTISMENT_CHOICES = [
        ('For_Sale', 'For Sale'), 
        ('To_Rent', 'To Rent'),
        ]
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    property_category = models.CharField(max_length=25,choices=PROPERTY_CATEGORY_CHOICES, default='STANDARD')
    property_type = models.CharField(max_length=100)
    advertised = models.CharField(max_length=10, choices=ADVERTISMENT_CHOICES, default='To_Rent')
    description = models.TextField(max_length=2000)
    short_description = models.TextField(max_length=150, default='')
    available_after = models.DateField(default=datetime.now)
    currency = models.CharField(max_length=10,choices=CURRENCY_CHOICES, default='€')
    price = models.IntegerField()
    bedrooms = models.DecimalField(max_digits=2, decimal_places=0)
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    furniture = models.CharField(max_length=11,choices=FURNITURE_CHOICES, default='Furnished')
    m2 = models.SmallIntegerField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', validators=[validate_file_size])
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, validators=[validate_file_size])
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, validators=[validate_file_size])
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, validators=[validate_file_size])
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, validators=[validate_file_size])
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    # Geocode
    street_number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postalcode = models.CharField(max_length=6, validators=[validate_postcode])
    admin_1 = models.CharField(max_length=100, blank=True)
    admin_1_en = models.CharField(max_length=100, blank= True)
    admin_2 = models.CharField(max_length=100, blank= True)
    admin_2_en = models.CharField(max_length=100, blank= True)
    admin_3 = models.CharField(max_length=100, blank= True)
    admin_3_en = models.CharField(max_length=100, blank= True)
    admin_4 = models.CharField(max_length=100, blank= True)
    admin_4_en = models.CharField(max_length=100, blank= True)
    country = models.CharField(max_length=100)
    country_en = models.CharField(max_length=100)
    geo_lat = models.CharField(max_length=15)
    geo_lng = models.CharField(max_length=15)
    identifier_1 = models.CharField(max_length=12)
    identifier_2 = models.CharField(max_length=12, blank=True)
    
    def __str__(self):
        
        return self.country
