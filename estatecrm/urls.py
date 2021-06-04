# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from properties.views import (PropertiesLandingListView, 
                              landing_autocomplete, 
                              create_autocomplete, 
                              base_layout, 
                              offline
                              )
from django.conf.urls.i18n import i18n_patterns



urlpatterns = [
    path('admin/', admin.site.urls),      
]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', PropertiesLandingListView.as_view(), name='landing-page'),
    path('base/', base_layout, name="base" ),
    path('offline/', offline, name="offline" ),
    path('accounts/', include('accounts.urls')),
    path('properties/', include('properties.urls', namespace='properties')),
    path('organisation/', include('realtors.urls', namespace='organisation')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',include('pwa.urls')), 
    re_path(r'^ajax/landing_autocomplete/$', landing_autocomplete, name = 'ajax_landing_autocomplete'),
    re_path(r'^ajax/create_autocomplete/$', create_autocomplete, name = 'ajax_create_autocomplete'),
    prefix_default_language=False,
)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

