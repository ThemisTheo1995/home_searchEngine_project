# properties/urls.py
from django.urls import path
from .views import (
    RealtorUpdateView, 
    RealtorDetailView,
    )

app_name = 'realtors'

urlpatterns =[
    path('<int:pk>/update/', RealtorUpdateView.as_view(), name='realtor-update'),
    path('<int:pk>/dashboard/', RealtorDetailView.as_view(), name='realtor-dashboard'),
]