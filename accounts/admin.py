# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_filter = ['is_active', 'is_superuser', 'is_staff']
    list_display = ['email', 'username', 'is_superuser', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['email']

    
