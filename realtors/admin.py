from django.contrib import admin
from .models import Realtor


@admin.register(Realtor)
class RealtorAdmin(admin.ModelAdmin):
    
    # form = PropertiesForm
    model = Realtor
    list_display = ['id','user']
    list_filter = ['user']
    list_display_links = ['id', 'user']
    # list_editable = ['is_published',]
    search_fields = ['id', 'user']
    list_per_page = 100