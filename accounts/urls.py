# accounts/urls.py
from django.urls import path
from .views import SignUpView, UpdateUserView, SettingsView

app_name = "accounts"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('update-user/', UpdateUserView.as_view(), name='update-user'),
    path('settings/', SettingsView.as_view(), name='settings'),
]