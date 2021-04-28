from django.contrib import admin
from .models import Properties
from .forms import PropertiesForm



@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    
    form = PropertiesForm
    model = Properties
    list_display = ['id', 'property_type','address', 'is_published', 'price', 'list_date', 'organisation']
    list_filter = ['advertised']
    list_display_links = ['id', 'address']
    list_editable = ['is_published',]
    search_fields = ['property_type', 'description', 'address', 'city', 'location', 'zipcode', 'price']
    list_per_page = 100
