# properties/urls.py
from django.urls import path, re_path
from .views import (
    PropertiesRentListView, 
    PropertiesDetailView,
    PropertiesCreateView,
    PropertiesUpdateView,
    rent_email_listview,
    properties_geoCreate,
    PropertiesSaleListView
    )

app_name = 'properties'

urlpatterns =[
    path('rent-list/', PropertiesRentListView.as_view(), name='rent-list'),
    path('property/<int:pk>/', PropertiesDetailView.as_view(), name='detail'),
    path('create/', PropertiesCreateView.as_view(), name='create' ),
    path('update/<int:pk>', PropertiesUpdateView.as_view(), name = 'update'),
    re_path(r'^ajax/rent_email_listview/$', rent_email_listview, name='ajax_rent_email_listview'),
    re_path(r'^ajax/properties_geoCreate/$', properties_geoCreate, name='ajax_properties_geoCreate'),
    path('sale-list/', PropertiesSaleListView.as_view(), name='sale-list'),
]