# properties/urls.py
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Properties
from .forms import FilterForm
from realtors.models import Realtor
    
### Landing views ###
class PropertiesLandingListView(generic.ListView):
    paginate_by = 4
    template_name = "landing.html"
    context_object_name = "landingProperties"
    
    def get_queryset(self):
        queryset = Properties.objects.filter(is_published= True).order_by('-list_date')[:16]
        return queryset

### Rent views ###
class PropertiesRentSearchView(generic.FormView):
    template_name = 'properties/properties_rent_search.html'
    form_class = FilterForm
    def get_success_url(self):
        return reverse('properties:rent-list')


class PropertiesRentListView(generic.ListView):
    paginate_by = 15
    template_name = "properties/properties_rent.html"
    context_object_name = "rentProperties"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['bathrooms'] = self.request.GET.get('bathrooms')
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        bathrooms = self.request.GET.get('bathrooms')
        object_all = Properties.objects.all()
        queryset = object_all.filter(
            city__icontains=city, 
            bathrooms__icontains=bathrooms,
            advertised = 'To_Rent',
            is_published=True,
            ).order_by('-list_date')
        return queryset


class PropertiesRentDetailView(generic.DetailView):
    template_name = "properties/properties_rent_detail.html"
    context_object_name = "rent"
    queryset = Properties.objects.filter(
            advertised = 'To_Rent',
            is_published=True,
            )
        
    