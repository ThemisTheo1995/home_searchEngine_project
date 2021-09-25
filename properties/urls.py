# properties/urls.py
from django.urls import path, re_path
from .views import (
    PropertiesRentListView, 
    PropertiesRentDetailView,
    PropertiesCreateView,
    PropertiesUpdateView,
    rent_email_listview,
    properties_geoCreate
    )

app_name = 'properties'

urlpatterns =[
    path('rent-list/', PropertiesRentListView.as_view(), name='rent-list'),
    path('property/<int:pk>/', PropertiesRentDetailView.as_view(), name='rent-detail'),
    path('create/', PropertiesCreateView.as_view(), name='create' ),
    path('update/<int:pk>', PropertiesUpdateView.as_view(), name = 'update'),
    re_path(r'^ajax/rent_email_listview/$', rent_email_listview, name='ajax_rent_email_listview'),
    re_path(r'^ajax/properties_geoCreate/$', properties_geoCreate, name='ajax_properties_geoCreate')
]