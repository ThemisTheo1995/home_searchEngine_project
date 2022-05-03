# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'is_realtor', 'is_agent', 'profile_picture')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_filter = ['is_active', 'is_superuser', 'is_staff', 'is_realtor', 'is_agent']
    list_display = ['email', 'username', 'is_active', 'is_realtor', 'is_agent','is_superuser']
    search_fields = ['email', 'username', 'is_active', 'is_realtor', 'is_agent']
    ordering = ['email']

    
