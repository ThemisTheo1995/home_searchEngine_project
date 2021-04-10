# properties/urls.py
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Properties
from .forms import FilterForm


class PropertiesRentSearchView(generic.FormView):
    template_name = 'properties/properties_rent_search.html'
    form_class = FilterForm
    def get_success_url(self):
        return reverse('properties:rent-list')


class PropertiesRentListView(generic.ListView):
    template_name = "properties/properties_rent.html"
    context_object_name = "rentProperties"

    def get_queryset(self):
        city = self.request.GET.get('city')
        bathrooms = self.request.GET.get('bathrooms')
        object_all = Properties.objects.all()
        queryset = object_all.filter(
            city__icontains=city, 
            bathrooms__icontains=bathrooms,
            for_sale=False, 
            to_rent=True, 
            is_published=True,
            )
        return queryset


class PropertiesRentDetailView(generic.DetailView):
    template_name = "properties/properties_rent_detail.html"
    context_object_name = "rent"
    queryset = Properties.objects.all()
        
    