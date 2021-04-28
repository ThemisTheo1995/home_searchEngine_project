# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from properties.views import PropertiesLandingListView
from django.conf.urls.i18n import i18n_patterns



urlpatterns = [
    path('admin/', admin.site.urls),       
]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', PropertiesLandingListView.as_view(), name='landing-page'),
    path('accounts/', include('accounts.urls')),
    path('properties/', include('properties.urls')),
    path('organisation/', include('realtors.urls', namespace='organisation')),
    path('accounts/', include('django.contrib.auth.urls')),
    prefix_default_language=False,
)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

