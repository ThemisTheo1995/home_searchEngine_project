# properties/urls.py
from django.urls import path
from .views import (
    OrganisationUpdateView, 
    OrganisationDashboardView,
    OrganisationProperties,
    AgentListView,
    AgentCreateView,
    )

app_name = 'realtors'

urlpatterns =[
    path('<int:pk>/update/', OrganisationUpdateView.as_view(), name = 'organisation-update'),
    path('<int:pk>/dashboard/', OrganisationDashboardView.as_view(), name = 'organisation-dashboard'),
    path('properties-list/', OrganisationProperties.as_view(), name = 'organisation-properties'),
    path('agent-list/', AgentListView.as_view(), name = 'agent-list'),
    path('agent-create/', AgentCreateView.as_view(), name = 'agent-create')
]