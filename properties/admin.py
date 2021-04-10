from django.contrib import admin
from .models import Properties



@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    
    model = Properties
    list_display = ['id', 'property_type','address', 'is_published', 'price', 'list_date', 'realtor']
    list_filter = ['for_sale','to_rent']
    list_display_links = ['id', 'address']
    list_editable = ['is_published',]
    search_fields = ['property_type', 'description', 'address', 'city', 'location', 'zipcode', 'price']
    list_per_page = 100
