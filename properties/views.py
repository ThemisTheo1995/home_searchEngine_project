# properties/urls.py
from django.views import generic
from estatecrm.keys import googleKey
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render,reverse, redirect
from .models import Properties
from .forms import FilterForm, PropertiesCreationForm
from urllib.parse import urlencode
from realtors import mixins
import requests, json

### Landing view ###
class PropertiesLandingListView(generic.ListView):
    paginate_by = 4
    template_name = "landing.html"
    context_object_name = "landingProperties"
    
    def get_queryset(self):
        queryset = Properties.objects.filter(is_published= True).order_by('-list_date')[:16]
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
                #Geocoding API
                endpoint = f"https://maps.googleapis.com/maps/api/geocode/json"
                params = {"address": location, "key": googleKey['GOOGLE_API_KEY']}
                
                #Parameters
                url_params = urlencode(params)
                url = f"{endpoint}?{url_params}"
                r = requests.get(url)
                if r.status_code not in range(200, 299): 
                    return Properties.objects.none()
                print(url)
                #JSON results
                results = r.json()['results']
                address_components = results[0]['address_components'][0].get("long_name")                
                country = results[0]['address_components'][-1].get("long_name")
                main_type = results[0].get("types")[0]
            else:
                return Properties.objects.none()
        
        if country and main_type == 'postal_code':  
            queryset = Properties.objects.filter(
                advertised = 'To_Rent',
                is_published=True,
                country = country,
                postalcode__icontains= address_components
                ).order_by('-list_date')
            return queryset
        elif country:
            queryset = Properties.objects.filter(
                advertised = 'To_Rent',
                is_published=True,
                country= country,
                search_address__icontains=address_components, 
                ).order_by('-list_date')
            return queryset
        else:
            queryset = Properties.objects.filter(
                advertised = 'To_Rent',
                is_published=True,
                search_address__icontains=address_components, 
                ).order_by('-list_date')
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
        if 'location' in self.request.POST:
            location = self.request.POST.get('location','')
            if len(location)>0: 
                #Geocoding API
                endpoint = f"https://maps.googleapis.com/maps/api/geocode/json"
                params = {"address": location, "key": googleKey['GOOGLE_API_KEY']}
                
                #Parameters
                url_params = urlencode(params)
                url = f"{endpoint}?{url_params}"
                r = requests.get(url)
                if r.status_code not in range(200, 299): 
                    return Properties.objects.none()
                
                #JSON results
                results = r.json()['results']
                
                #Main location type (main_type in model)
                if results[0]['types'][0]:
                    main_type = results[0]['types'][0]
                else: main_type = ''
                
                #Search address
                search_address = ''
                
                #Formatted address
                formatted_address = results[0].get("formatted_address")
                    
                #Location types
                if results[0]['address_components']:
                    address_components = results[0]['address_components']
                    propertyAddressArray = {}
                    for components in address_components:
                        
                        if components.get("types")[0] == 'street_number':
                            propertyAddressArray['street_number'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'premise':
                            propertyAddressArray['premise'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'country':
                            propertyAddressArray['country'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                            
                        elif components.get("types")[0] == 'route':
                            propertyAddressArray['route'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'political':
                            propertyAddressArray['political'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'locality':
                            propertyAddressArray['locality'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'postal_town':
                            propertyAddressArray['postal_town'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "

                        elif components.get("types")[0] == 'administrative_area_level_1':
                            propertyAddressArray['administrative_area_level_1'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'administrative_area_level_2':
                            propertyAddressArray['administrative_area_level_2'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'administrative_area_level_3':
                            propertyAddressArray['administrative_area_level_3'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'administrative_area_level_4':
                            propertyAddressArray['administrative_area_level_4'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'administrative_area_level_5':
                            propertyAddressArray['administrative_area_level_5'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "
                        
                        elif components.get("types")[0] == 'postal_code':
                            propertyAddressArray['postalcode'] = components.get("long_name")
                            search_address += components.get("long_name") +  ", "

                #Lat/Lng
                if results[0]['geometry']['location']:
                    propertyAddressArray['geo_lat'] = results[0]['geometry']['location'].get('lat')
                    propertyAddressArray['geo_lng'] = results[0]['geometry']['location'].get('lat')

                print(f"{search_address}")
        
        # Excluded form fields, manually saved
        properties.organisation = self.request.user.organisation
        properties.search_address = search_address
        properties.formatted_address = formatted_address
        properties.premise = propertyAddressArray['premise'] if "premise" in propertyAddressArray else ''
        properties.street_number = propertyAddressArray['street_number'] if "street_number" in propertyAddressArray else ''
        properties.route = propertyAddressArray['route'] if "route" in propertyAddressArray else ''
        properties.political = propertyAddressArray['political'] if "political" in propertyAddressArray else ''
        properties.locality = propertyAddressArray['locality'] if "locality" in propertyAddressArray else ''
        properties.postal_town = propertyAddressArray['postal_town'] if "postal_town" in propertyAddressArray else ''
        properties.neighborhood = propertyAddressArray['neighborhood'] if "neighborhood" in propertyAddressArray else ''
        properties.administrative_area_level_1 = propertyAddressArray['administrative_area_level_1'] if "administrative_area_level_1" in propertyAddressArray else ''
        properties.administrative_area_level_2 = propertyAddressArray['administrative_area_level_2'] if "administrative_area_level_2" in propertyAddressArray else ''
        properties.administrative_area_level_3 = propertyAddressArray['administrative_area_level_3'] if "administrative_area_level_3" in propertyAddressArray else ''
        properties.administrative_area_level_4 = propertyAddressArray['administrative_area_level_4'] if "administrative_area_level_4" in propertyAddressArray else ''
        properties.administrative_area_level_5 = propertyAddressArray['administrative_area_level_5'] if "administrative_area_level_5" in propertyAddressArray else ''
        properties.postalcode = propertyAddressArray['postalcode']
        properties.geo_lat = propertyAddressArray['geo_lat']
        properties.geo_lng = propertyAddressArray['geo_lng'] 
        properties.country = propertyAddressArray['country']
        properties.main_type = main_type
        properties.save()
        
        return super(PropertiesCreateView, self).form_valid(form)

    
    