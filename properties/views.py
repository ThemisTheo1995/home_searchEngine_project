# properties/urls.py
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Properties


class PropertiesRentListView(generic.ListView):
    template_name = "properties/properties_rent.html"
    context_object_name = "rentProperties"
    queryset = Properties.objects.filter(for_sale=False, to_rent=True)