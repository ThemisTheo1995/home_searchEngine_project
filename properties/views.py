# properties/views.py
from django.views import generic
from django.http import JsonResponse
from estatecrm.keys import googleKey
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.db.models import Q
from django.core import serializers
from django.shortcuts import reverse, get_object_or_404, render
from .models import Properties, geoData
from .forms import FilterForm, PropertiesCreationForm, PropertiesUpdateForm
from urllib.parse import urlencode
from realtors import mixins
import requests, json, re 

### Offline view ###
def offline(request):
    template='offline.html'
    return render(request,template) 

### Base view ###
def base_layout(request):
    template='base.html'
    return render(request,template)   

### Landing view - Auto complete ###
def landing_autocomplete(request):
    if  request.method == 'GET':
        location_data = geoData.objects.all().order_by('identifier','-location')
        raw_data = serializers.serialize("python", location_data)
        actual_data = [data['fields'] for data in raw_data]
        return JsonResponse(actual_data, safe=False)
        
### Landing view ###
class PropertiesLandingListView(generic.ListView):
    paginate_by = 4
    template_name = "landing.html"
    context_object_name = "landingProperties"
    
    def get_queryset(self):
        queryset = Properties.objects.filter(is_published= True).order_by('-list_date')[:4]
        return queryset

### Rent List view ###
class PropertiesRentListView(generic.ListView):
    paginate_by =22
    template_name = "properties/properties_rent.html"
    context_object_name = "rentProperties"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = self.request.GET.get('address','')
        context['bathrooms'] = self.request.GET.get('bathrooms','')
        context['location'] = self.request.GET.get('location','')
        
        return context

    def get_queryset(self):
        if 'location' in self.request.GET:
            location = self.request.GET.get('location','')
            address = self.request.GET.get('address','')
            bathrooms = self.request.GET.get('bathrooms','')
            if len(location)>0: 
                # Check if the identifier exists
                try:
                    identifier = geoData.objects.get(Q(location=location) | Q(location_en = location)).identifier
                    if identifier:
                        identifier = identifier.split("-")
                        try: 
                            identifier = identifier[0]+'-'+identifier[1]
                            queryset = Properties.objects.filter(identifier__identifier = identifier, is_published=True, advertised='To_Rent')
                        except:
                            identifier = identifier[0]
                            queryset = Properties.objects.filter(identifier__identifier__startswith=identifier, is_published=True, advertised='To_Rent')
                    else:
                        queryset = Properties.objects.none()
                except geoData.DoesNotExist:
                    identifier = None
                    queryset = Properties.objects.none()
            else: queryset = Properties.objects.none()
            
        return queryset

### Rent Detail view ###
class PropertiesRentDetailView(generic.DetailView):
    template_name = "properties/properties_rent_detail.html"
    context_object_name = "rent"
    queryset = Properties.objects.filter(
            advertised = 'To_Rent',
            is_published=True,
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        try:
            prop_features_json = Properties.objects.get(pk=pk).property_features
            if prop_features_json:
                jsonDec = json.decoder.JSONDecoder()
                prop_features = jsonDec.decode(prop_features_json)
                if prop_features:
                    for value in prop_features:
                        context[value] = value
        except Properties.DoesNotExist:
            context[''] = ''
        
        return context
    

### Create view - Auto complete ###
def create_autocomplete(request):
    if  request.method == 'GET':
        location_data = geoData.objects.exclude(identifier__isnull=True).exclude(identifier__exact='').order_by('identifier','-location')
        raw_data = serializers.serialize("python", location_data)
        actual_data = [data['fields'] for data in raw_data]
        return JsonResponse(actual_data, safe=False)

### Rent Create view ###
class PropertiesCreateView(mixins.OrganisationAndLoginRequiredMixin, generic.CreateView):
    template_name = "properties/properties_create.html"
    form_class = PropertiesCreationForm
    
    def get_success_url(self):
        return reverse("organisation:organisation-properties")
    
    def form_valid(self, form):
        properties = form.save(commit = False)
        if 'location-create' and 'address' in self.request.POST:
            location = self.request.POST.get('location-create','')
            address_search = self.request.POST.get('address', '')
            property_features = self.request.POST.getlist('property-features','')
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
                #Lat long
                geo_lat = latlng.get("lat")
                geo_lng = latlng.get("lng")
                
                results = r.json()['results'][0]["address_components"]
                #Number
                if  results[0]['types'][0] == "street_number":
                    street_number = results[0].get("long_name")
                else:
                    return reverse_lazy("properties:create")
                #Address
                if  results[1]['types'][0] == "route":
                    address = results[1].get("long_name")
                else:
                    return reverse_lazy("properties:create")
                
                #Main location query
                try:
                    location_info = geoData.objects.get(Q(location=location) | Q(location_en = location))
                except:
                    return reverse_lazy("properties:create")
                
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
                #Identifier
                if location_info.identifier:
                    identifier = location_info.identifier
                else:
                    identifier =''
                
                if property_features:
                    property_features = json.dumps(property_features)
                    
        # Excluded form fields, manually saved
        properties.organisation = self.request.user.organisation
        properties.property_features = property_features
        properties.street_number = street_number
        properties.geo_lat = geo_lat
        properties.geo_lng = geo_lng
        properties.address = address
        properties.country = country
        properties.country_en = country_en
        properties.admin_1 = admin_1
        properties.admin_1_en = admin_1_en
        properties.admin_2 = admin_2
        properties.admin_2_en = admin_2_en
        properties.admin_3 = admin_3
        properties.admin_3_en = admin_3_en
        properties.admin_4 = admin_4
        properties.admin_4_en = admin_4_en
        properties.identifier = location_info
    
        properties.save()
        
        return super(PropertiesCreateView, self).form_valid(form)

### Rent Update view ###
class PropertiesUpdateView(mixins.OrganisationAndLoginRequiredMixin, generic.UpdateView):
    template_name = "properties/properties_update.html"
    form_class = PropertiesUpdateForm
    model = Properties
    context_object_name = "property"
    
    def get_success_url(self):
        return reverse("organisation:organisation-properties")
    
    def get_queryset(self): 
        organisation = self.request.user.organisation
        return Properties.objects.filter(organisation=organisation)

    def get_context_data(self, **kwargs):
        context = super(PropertiesUpdateView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        try:
            proper = Properties.objects.get(id=pk)
        except Properties.DoesNotExist:
            proper = None
        location = proper.identifier.location

        context['location'] = location
        
        return context
    
    def form_valid(self, form):
        properties = form.save(commit = False)
        if 'location-update' in self.request.POST:
            location = self.request.POST.get('location-update','')
            if len(location)>0: 

                #Main location query
                try:
                    location_info = geoData.objects.get(Q(location=location) | Q(location_en = location))
                except:
                    return reverse_lazy("properties:update")
                
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
                
                #Identifier
                if location_info.identifier:
                    identifier = location_info.identifier
                else:
                    identifier =''

        # Excluded form fields => manually saved
        properties.organisation = self.request.user.organisation
        properties.country = country
        properties.country_en = country_en
        properties.admin_1 = admin_1
        properties.admin_1_en = admin_1_en
        properties.admin_2 = admin_2
        properties.admin_2_en = admin_2_en
        properties.admin_3 = admin_3
        properties.admin_3_en = admin_3_en
        properties.admin_4 = admin_4
        properties.admin_4_en = admin_4_en
        properties.identifier = location_info
        properties.save()
        
        return super(PropertiesUpdateView, self).form_valid(form)
   
    