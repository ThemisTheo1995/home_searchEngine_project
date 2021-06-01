# properties/urls.py
from django.urls import path, re_path
from .views import (
    OrganisationUpdateView, 
    OrganisationDashboardView,
    OrganisationProperties,
    AgentListView,
    AgentCreateView,
    realtors_org_rent_preview
    )

app_name = 'realtors'

urlpatterns =[
    path('<int:pk>/update/', OrganisationUpdateView.as_view(), name = 'organisation-update'),
    path('<int:pk>/dashboard/', OrganisationDashboardView.as_view(), name = 'organisation-dashboard'),
    path('properties-list/', OrganisationProperties.as_view(), name = 'organisation-properties'),
    path('agent-list/', AgentListView.as_view(), name = 'agent-list'),
    path('agent-create/', AgentCreateView.as_view(), name = 'agent-create'),
    re_path(r'^ajax/realtors_org_rent_preview/$', realtors_org_rent_preview, name = 'ajax_realtors_org_rent_preview'),
]