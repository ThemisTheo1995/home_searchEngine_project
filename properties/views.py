# properties/urls.py
from django.views import generic
from django.http import JsonResponse
from estatecrm.keys import googleKey, mapBoxKey
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render,reverse, redirect
from .models import Properties
from .forms import FilterForm, PropertiesCreationForm
from urllib.parse import urlencode
from realtors import mixins
import requests, json

### Landing view ###
def landing_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('q', '')
        country = list(Properties.objects.filter(country__startswith = q).values_list('country', flat=True))
        print(country)
        data = {
            'country': country,
        }
        return JsonResponse(data)

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
                #Geocoding API
                addressText = {"address": location + '.json'}
                endpoint = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{urlencode(addressText)}"
                params = {"access_token": 'pk.eyJ1IjoidGhlbWlzdGhlbzE5OTUiLCJhIjoiY2tidGlyZ2xrMGE1aDJ6bWkzZnlwM2t4aiJ9.QZXJ0ujvaC2sScu_VmT9zg'}
                
                #Parameters
                url_params = urlencode(params)
                url = f"{endpoint}?{url_params}"
                r = requests.get(url)
                if r.status_code not in range(200, 299): 
                    return Properties.objects.none()
                #JSON results
                results = r.json()
                country = results['features'][0]['context'][-1]['short_code']
                address = results['features'][0]['text']
                print(url)
                if results['features'][0]['place_type'] == 'postcode':
                    main_type = 'postcode'
                else: main_type = ''
                
            else:
                return Properties.objects.none()
        
        if country and main_type == 'postcode':  
            queryset = Properties.objects.filter(
                advertised = 'To_Rent',
                is_published=True,
                country = country,
                postalcode__icontains= address
                ).order_by('-list_date')
            return queryset
        elif country:
            queryset = Properties.objects.filter(
                advertised = 'To_Rent',
                is_published=True,
                country= country,
                search_address__icontains=address, 
                ).order_by('-list_date')
            return queryset
        else:
            queryset = Properties.objects.filter(
                advertised = 'To_Rent',
                is_published=True,
                search_address__icontains=address, 
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
            print(location)
            if len(location)>0: 
                
                # ### Google Geo endpoint ###
                # endpoint = f"https://maps.googleapis.com/maps/api/geocode/json"
                # params = {"address": location, "key": googleKey['GOOGLE_API_KEY']}
                
                # #Parameters
                # url_params = urlencode(params)
                # url = f"{endpoint}?{url_params}"
                # r = requests.get(url)
                # print(url)
                # if r.status_code not in range(200, 299): 
                #     return reverse_lazy("properties:create")
                
                # #Returned google JSON
                # results = r.json()['results']
                
                ### MapBox Geo endpoint ###
                print(location)
                geo = location.split(",")
                endpointMapBox = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{geo[0]},{geo[1]}.json"
                paramsMapBox = {"access_token": mapBoxKey['MAPBOX_API_KEY']}
                
                #Parameters
                url_paramsMapBox = urlencode(paramsMapBox)
                urlMapBox = f"{endpointMapBox}?{url_paramsMapBox}"
                rMapBox = requests.get(urlMapBox)
                print(urlMapBox)
                if rMapBox.status_code not in range(200, 299): 
                    return reverse_lazy("properties:create")
                
                #Returned mapbox JSON
                resultsMapBox = rMapBox.json()
                
                #Search address
                search_address = ''
                
                #Country (mandatory field)
                if resultsMapBox['features'][0]['context'][-1]['text']:
                    country = resultsMapBox['features'][0]['context'][-1]['short_code']
                else: 
                    return reverse_lazy("properties:create")
                
                if resultsMapBox['features'][0]['place_name'] or resultsMapBox['features'][0]['place_name'] :
                    search_address += resultsMapBox['features'][0]['place_name'] +  ", "

                print(f"{search_address}")
        
        # Excluded form fields, manually saved
        properties.organisation = self.request.user.organisation
        properties.search_address = search_address
        properties.geo_lat = geo[1]
        properties.geo_lng = geo[0]
        properties.country = country
        properties.save()
        
        return super(PropertiesCreateView, self).form_valid(form)

    
    