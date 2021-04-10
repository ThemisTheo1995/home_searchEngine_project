# properties/urls.py
from django.urls import path
from .views import (
    PropertiesRentListView, 
    PropertiesRentSearchView,
    PropertiesRentDetailView
    )

app_name = 'properties'

urlpatterns =[
    path('rent-search/', PropertiesRentSearchView.as_view(), name='rent-search'),
    path('rent-list/', PropertiesRentListView.as_view(), name='rent-list'),
    path('<int:pk>/', PropertiesRentDetailView.as_view(), name='rent-detail'),
]