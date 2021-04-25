# properties/urls.py
from django.urls import path
from .views import (
    RealtorUpdateView, 
    RealtorDashboardView,
    RealtorProperties
    )

app_name = 'realtors'

urlpatterns =[
    path('<int:pk>/update/', RealtorUpdateView.as_view(), name = 'realtor-update'),
    path('<int:pk>/dashboard/', RealtorDashboardView.as_view(), name = 'realtor-dashboard'),
    path('<int:pk>/properties-list/', RealtorProperties.as_view(), name = 'realtor-properties')
]