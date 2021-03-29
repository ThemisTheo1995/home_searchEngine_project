# properties/urls.py
from django.urls import path
from .views import PropertiesRentListView

app_name = 'properties'

urlpatterns =[
    path('rent/', PropertiesRentListView.as_view(), name='rent'),
]