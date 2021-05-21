from django.contrib import admin
from .models import Properties, geoData
from .forms import PropertiesForm
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# GeoData admin
class geoDataResource(resources.ModelResource):
    class Meta:
        model = geoData

@admin.register(geoData)
class geoDataAdmin(ImportExportModelAdmin):
    resource_class = geoDataResource
    list_display = ['id', 'location', 'location_en', 'identifier']
    search_fields = ['location_en', 'location', 'identifier']

# Properties admin
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
