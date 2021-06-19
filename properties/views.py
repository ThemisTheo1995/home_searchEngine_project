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
from .choices import (price_rent_choices,
                      type_rent_choices, 
                      furniture_choices, 
                      order_list_date_choices, 
                      order_price_choices,
                      pagination_choices)

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
    paginate_by =15
    template_name = "properties/properties_list.html"
    context_object_name = "rentProperties"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pre = self.request.GET.get
        context['location'] = pre('location', '')
        context['minbathrooms'] = pre('minbaths','')
        context['minbedrooms'] = pre('minbeds','')
        context['maxbathrooms'] = pre('maxbaths','')
        context['maxbedrooms'] = pre('maxbeds','')
        context['minprice'] = pre('minprice','')
        context['maxprice'] = pre('maxprice','')
        context['type'] = pre('type','')
        context['furniture'] = pre('furniture','')
        context['price'] = price_rent_choices
        context['type_choices'] = type_rent_choices
        context['furniture_choices'] = furniture_choices
        context['order_list_date_choices'] = order_list_date_choices
        context['orderlist'] = pre('orderlist','')
        context['order_price_choices'] = order_price_choices
        context['orderprice'] = pre('orderprice','')
        context['views'] = pre('views','')
        context['pagination_choices'] = pagination_choices
        context['paginate_by'] = pre('paginate_by', 15) or 15
        try:
            if len(context['rentProperties'])>0:
                markerSet = []
                for M in context['rentProperties']:
                    markerSet.append([M.address,float(M.geo_lat), float(M.geo_lng), M.pk, M.organisation.name])
            context['markerSet'] = markerSet
        except:
            context['markerSet'] = "undefined"
        
        return context

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        if 'location' in self.request.GET:
            pre = self.request.GET.get
            # Parameters
            location = pre('location','')
            minbeds = pre('minbeds','')
            minbaths = pre('minbaths','')
            maxbeds = pre('maxbeds','')
            maxbaths = pre('maxbaths','')
            maxprice = pre('maxprice','')
            minprice = pre('minprice','')
            prop_type = pre('type','')
            furniture = pre('furniture','')
            orderlist = pre('orderlist','')
            orderprice = pre('orderprice','')
            # Location filter
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
            # Bathrooms filter
            minbaths = int(minprice) if minbaths != '' else ''
            maxbaths = int(maxprice) if maxbaths != '' else ''
            if minbaths != '' and maxbaths != '' and (minbaths > -1 and minbaths < 99) and (maxbaths > -1 and maxbaths < 99):
                try:
                    queryset = queryset.filter(bathrooms__gte = minbaths, bathrooms__lte = maxbaths)
                except:pass
            elif minbaths != '' and (minbaths > -1 and minbaths < 99):
                try:
                    queryset = queryset.filter(bathrooms__gte = minbaths)
                except:pass
            elif maxbaths != '' and (maxbaths > -1 and maxbaths < 99):
                try:
                    queryset = queryset.filter(bathrooms__lte = maxbaths)
                except:pass
            # Bedrooms filter
            minbeds = int(minbeds) if minbeds != '' else ''
            maxbeds = int(maxbeds) if maxbeds != '' else ''
            if minbeds != '' and maxbeds != '' and (minbeds > -1 and minbeds < 99) and (maxbeds > -1 and maxbeds < 99):
                try:
                    queryset = queryset.filter(bathrooms__gte = minbeds, bathrooms__lte = maxbeds)
                except:pass
            elif minbeds != '' and (minbeds > -1 and minbeds < 99):
                try:
                    queryset = queryset.filter(bathrooms__gte = minbeds)
                except:pass
            elif maxbeds !='' and (maxbeds > -1 and maxbeds < 99):
                try:
                    queryset = queryset.filter(bathrooms__lte = maxbeds)
                except:pass
            # Price filter
            minprice = int(minprice) if minprice != '' else ''
            maxprice = int(maxprice) if maxprice != '' else ''
            if minprice != '' and maxprice != '' and (minprice > 49 and minprice < 10001) and (maxprice > 49 and maxprice < 10001):
                try:
                    queryset = queryset.filter(price__gte = minprice, price__lte = maxprice)
                except:pass
            elif minprice != '' and (minprice > 49 and minprice < 10001):
                try:
                    queryset = queryset.filter(price__gte = minprice)
                except:pass
            elif maxprice !='' and (maxprice > 49 and maxprice < 10001):
                try:
                    queryset = queryset.filter(price__lte = maxprice)
                except:pass
            # Property type filter
            if prop_type != '' and type(prop_type)==str:
                try:
                    queryset = queryset.filter(property_type = prop_type)
                except:pass
        return queryset

### Rent Detail view ###
class PropertiesRentDetailView(generic.DetailView):
    template_name = "properties/properties_detail.html"
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
   
    