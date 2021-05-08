# properties/urls.py
from django.urls import path
from .views import (
    PropertiesRentListView, 
    PropertiesRentDetailView,
    PropertiesCreateView
    )

app_name = 'properties'

urlpatterns =[
    path('rent-list/', PropertiesRentListView.as_view(), name='rent-list'),
    path('<int:pk>/', PropertiesRentDetailView.as_view(), name='rent-detail'),
    path('create/', PropertiesCreateView.as_view(), name='create' )
]