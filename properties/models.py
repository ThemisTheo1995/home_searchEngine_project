# properties/models.py
from django.db import models
from io import BytesIO
import sys
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from accounts.models import CustomUser 
from datetime import datetime
from PIL import Image, ImageOps
from .validators import validate_file_size, validate_postcode
from realtors.models import Organisation,Agent
from django.core.files.uploadedfile import InMemoryUploadedFile
from sorl.thumbnail import ImageField


#geoData model
class geoData(models.Model):
    
    country = models.CharField(max_length=100, blank=True)
    country_en = models.CharField(max_length=100, blank=True)
    admin_1 = models.CharField(max_length=100, blank=True, default='')
    admin_1_en = models.CharField(max_length=100, blank=True, default='')
    admin_2 = models.CharField(max_length=100, blank=True)
    admin_2_en = models.CharField(max_length=100, blank=True)
    admin_3 = models.CharField(max_length=100, blank=True)
    admin_3_en = models.CharField(max_length=100, blank=True)
    admin_4 = models.CharField(max_length=100, blank=True)
    admin_4_en = models.CharField(max_length=100, blank=True)
    identifier = models.CharField(max_length=100, blank=True, default='')
    location = models.CharField(max_length=250, blank=True)
    location_en = models.CharField(max_length=250, blank=True)
    
    def save(self, *args, **kwargs):
        
        if not self.admin_1:  
            self.location = self.admin_2 + ', ' + self.admin_3 + ', ' + self.country 
        else: 
            self.location = self.admin_1 + ', ' + self.admin_2 + ', ' + self.admin_3 + ', ' + self.country
        
        if not self.admin_1_en:
            self.location_en = self.admin_2_en + ', ' + self.admin_3_en + ', ' + self.country_en
        else:
            self.location_en = self.admin_1_en + ', ' + self.admin_2_en + ', ' + self.admin_3_en + ', ' + self.country_en
        super(geoData, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.identifier}"

#Signal to generate the identifier
def update_identifier(sender, instance, **kwargs):
    if instance.admin_2_en or instance.admin_2:
        try:
            parent_pk = geoData.objects.get(country=instance.country,
                                            admin_4=instance.admin_4,
                                            admin_3=instance.admin_3,
                                            admin_2=instance.admin_2,
                                            admin_1 = '').pk
            parent_pk = str(parent_pk)
        except geoData.DoesNotExist:
            parent_pk = None
        
        if instance.admin_1 == '' and instance.admin_1_en == '' and parent_pk == str(instance.pk):
            new_identifier = instance.pk
        elif parent_pk is not None and (instance.admin_1 or instance.admin_1_en):
            new_identifier = parent_pk+'-'+str(instance.pk)
        else:
            new_identifier =''
            
    geoData.objects.filter(pk=instance.pk).update(identifier=new_identifier)

post_save.connect(update_identifier, sender=geoData)

#Properties model
class Properties(models.Model):
    TYPE_CHOICES = [
        ('Flat/Apartment', _('Flat/Apartment')),
        ('Cottage', _('Cottage')),
        ('Detached', _('Detached')),
        ('Semi-Detached', _('Semi-Detached')),
        ('Terraced', _('Terraced')),
        ('Studio', _('Studio')),
        ('Bungalow', _('Bungalow')),
        ('Penthouse', _('Penthouse')),
        ('Land', _('Land')),
        ('Shared', _('Shared')),
    ]
    FURNITURE_CHOICES = [
        ('Furnished', _('Furnished')),
        ('Unfurnished', _('Unfurnished')),
    ]
    CURRENCY_CHOICES = [
        ('???', 'EUR(???)'),
        ('??', 'GBP(??)'),
        ('$', 'USD($)'),
    ]
    PROPERTY_CATEGORY_CHOICES = [
        ('FEATURED', _('FEATURED')),
        ('OPPORTUNITY', _('OPPORTUNITY')),
        ('STANDARD', _('STANDARD')),        
    ]
    ADVERTISMENT_CHOICES = [
        ('For_Sale', _('For Sale')), 
        ('To_Rent', _('To Rent')),
        ]
    FEATURE = [
        ('', ''),
        ('Energy Efficient', _('Energy Efficient')),
        ('Garage', _('Garage')),
        ('Open Plan', _('Open Plan')),
        ('New Construction', _('New Construction')),
        ('Modern', _('Modern')),
        ('Classic', _('Classic')),
        ('Fireplace', _('Fireplace')),
        ('Garden', _('Garden')),
    ]
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    property_category = models.CharField(max_length=25,choices=PROPERTY_CATEGORY_CHOICES, default='STANDARD')
    property_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='Flat/Apartment')
    property_feature = models.CharField(max_length=100, choices=FEATURE, default = '', blank=True)
    property_features = models.CharField(max_length=300, blank=True, default='')
    advertised = models.CharField(max_length=10, choices=ADVERTISMENT_CHOICES, default='To_Rent')
    description = models.TextField(max_length=2000)
    short_description = models.TextField(max_length=180, default='')
    available_after = models.DateField(default=datetime.now)
    currency = models.CharField(max_length=10,choices=CURRENCY_CHOICES, default='???')
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
    street_number = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
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
    identifier = models.ForeignKey(geoData, models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.photo_main:
            self.photo_main = self.compressImage(self.photo_main)
        if self.photo_1:
            self.photo_1 = self.compressImage(self.photo_1)
        if self.photo_2:
            self.photo_2 = self.compressImage(self.photo_2)
        if self.photo_3:
            self.photo_3 = self.compressImage(self.photo_3)
        if self.photo_4:
            self.photo_4 = self.compressImage(self.photo_4)
        super(Properties, self).save(*args, **kwargs)
    
    
    def compressImage(self,photo):
        imageTemporary = Image.open(photo)
        outputIoStream = BytesIO()
        imageTemporaryResized = ImageOps.exif_transpose(imageTemporary) 
        if imageTemporaryResized.height/imageTemporaryResized.width>1:
            imageTemporaryResized = imageTemporaryResized.resize( (600,1000) )
        else:
            imageTemporaryResized = imageTemporaryResized.resize( (1000,600) )  
        imageTemporaryResized.save(outputIoStream , format='JPEG', quality=50)
        outputIoStream.seek(0)
        photo = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % photo.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return photo
    
    def __str__(self):
        
        return self.address

class UserPropertyFavourite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    favourite = models.ForeignKey(Properties, on_delete = models.CASCADE)
    notes = models.TextField(max_length=1500, blank=True)
    
    def __str__(self):
        return self.favourite