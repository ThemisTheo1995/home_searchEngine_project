from django.contrib import admin
from .models import Properties
from .forms import PropertiesForm



@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    
    form = PropertiesForm
    model = Properties
    list_display = ['id', 'organisation', 'property_type','is_published', 'price', 'list_date', 'country']
    list_filter = ['advertised', 'organisation', 'country', 'property_type', 'price', 'list_date']
    list_display_links = ['id']
    list_editable = ['is_published',]
    search_fields = ['property_type', 'description', 'country', 'postalcode', 'price']
    list_per_page = 100
