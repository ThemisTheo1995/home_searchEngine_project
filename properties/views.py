# properties/urls.py
from django.views import generic
from django.http import JsonResponse
from estatecrm.keys import googleKey, mapBoxKey
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.db.models import Q
from django.core import serializers
from django.core.serializers.json import Serializer as DjangoSerializer
from django.shortcuts import render,reverse, redirect
from .models import Properties, geoSearch, geoData
from .forms import FilterForm, PropertiesCreationForm
from urllib.parse import urlencode
from realtors import mixins
import requests, json
    
### Landing view ###
def landing_autocomplete(request):
    if request:
        location_data = geoSearch.objects.all().order_by('-identifier','-location')
        raw_data = serializers.serialize("python", location_data)
        actual_data = [data['fields'] for data in raw_data]
        
        return JsonResponse(actual_data, safe=False)

class PropertiesLandingListView(generic.ListView):
    paginate_by = 4
    template_name = "landing.html"
    context_object_name = "landingProperties"
    
    def get_queryset(self):
        queryset = Properties.objects.filter(is_published= True).order_by('-list_date')[:4]
        return queryset

### Rent List view ###
class PropertiesRentListView(generic.ListView):
    paginate_by = 15
    template_name = "properties/properties_rent.html"
    context_object_name = "rentProperties"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city','')
        context['bathrooms'] = self.request.GET.get('bathrooms','')
        return context

    def get_queryset(self):
        if 'location' in self.request.GET:
            location = self.request.GET.get('location','')
            if len(location)>0: 
                # Check if the identifier exists
                try:
                    identifier = geoSearch.objects.get(location=location).identifier
                    contains_digit = False
                    for char in identifier:
                        if char.isdigit():
                            contains_digit = True
                    if contains_digit:
                        queryset = Properties.objects.filter(identifier_2=identifier)
                    else:
                        queryset = Properties.objects.filter(Q(identifier_1=identifier) | Q(identifier_2__icontains = identifier))
                except geoSearch.DoesNotExist:
                    identifier = None
                    queryset = Properties.objects.none()

        return queryset

### Rent Detail view ###
class PropertiesRentDetailView(generic.DetailView):
    template_name = "properties/properties_rent_detail.html"
    context_object_name = "rent"
    queryset = Properties.objects.filter(
            advertised = 'To_Rent',
            is_published=True,
            )

### Rent Create view ###
class PropertiesCreateView(mixins.OrganisationAndLoginRequiredMixin, generic.CreateView):
    template_name = "properties/properties_create.html"
    form_class = PropertiesCreationForm
    
    def get_success_url(self):
        return reverse("organisation:organisation-properties")
    
    def form_valid(self, form):
        properties = form.save(commit = False)
        if 'location' and 'address' in self.request.POST:
            location = self.request.POST.get('location','')
            address_search = self.request.POST.get('address', '')
            if len(location)>0 and len(address_search)>0: 
                
                ### Google Geo endpoint ###
                endpoint = f"https://maps.googleapis.com/maps/api/geocode/json"
                params = {"address": address_search, "key": googleKey['GOOGLE_API_KEY']}
                
                #Parameters
                url_params = urlencode(params)
                url = f"{endpoint}?{url_params}"
                r = requests.get(url)
                if r.status_code not in range(200, 299): 
                    return reverse_lazy("properties:create")
                
                #Returned google JSON - lat long
                latlng = r.json()['results'][0]['geometry']['location']
                # Lat long
                geo_lat = latlng.get("lat")
                geo_lng = latlng.get("lng")
                
                #Main location query
                location_search_identifier = geoSearch.objects.get(location=location).identifier
                location_info = geoData.objects.get(identifier=location_search_identifier)
                
                #Country
                country = location_info.country
                country_en = location_info.country_en
                
                #Admin areas
                admin_1 = location_info.admin_1
                admin_1_en = location_info.admin_1_en
                admin_2 = location_info.admin_2
                admin_2_en = location_info.admin_2_en
                admin_3 = location_info.admin_3
                admin_3_en = location_info.admin_3_en
                admin_4 = location_info.admin_4
                admin_4_en = location_info.admin_4_en
                
                #Identifiers
                try:
                    contains_digit = False
                    for char in location_info.identifier:
                        if char.isdigit():
                            contains_digit = True
                    if contains_digit:
                        identifier_1 = location_info.identifier[5:]
                        identifier_2 = location_info.identifier
                    else:
                        identifier_1 = location_info.identifier
                        identifier_2 = ''
                except location_info.identifier is None:
                    return reverse_lazy("properties:create")

        # Excluded form fields, manually saved
        properties.organisation = self.request.user.organisation
        properties.street_number = '64'
        properties.geo_lat = geo_lat
        properties.geo_lng = geo_lng
        properties.address = 'Agiou Gerasimou'
        properties.country = country
        properties.country_en = country_en
        properties.admin_1 = admin_1,
        properties.admin_1_en = admin_1_en,
        properties.admin_2 = admin_2,
        properties.admin_2_en = admin_2_en,
        properties.admin_3 = admin_3,
        properties.admin_3_en = admin_3_en,
        properties.admin_4 = admin_4,
        properties.admin_4_en = admin_4_en,
        properties.identifier_1 = identifier_1
        properties.identifier_2 = identifier_2
    
        properties.save()
        
        return super(PropertiesCreateView, self).form_valid(form)

    
    