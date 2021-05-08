from django.contrib import admin
from .models import Organisation, Agent


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    
    # form = PropertiesForm
    model = Organisation
    list_display = ['id','user','name','email', 'list_date']
    list_filter = ['user']
    list_display_links = ['id', 'user', 'name']
    # list_editable = ['is_published',]
    search_fields = ['id', 'user']
    list_per_page = 100
    
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    
    #form = AgentModelAddForm
    model = Agent
    list_display = ['id','user','organisation', 'list_date']
    list_filter = ['user']
    list_display_links = ['id', 'user']
    search_fields = ['id', 'user', 'organisation']
    list_per_page = 100