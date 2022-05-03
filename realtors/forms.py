# realtors/forms
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from .models import Organisation

class OrganisationUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Organisation
        fields = ('name', 'email', 'phone', 'email', 
                  'country_code', 'organisation_description',
                  'organisation_logo')

class AgentModelAddForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'profile_picture'
        )   
