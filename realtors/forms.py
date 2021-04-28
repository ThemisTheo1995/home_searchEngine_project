# realtors/forms
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from accounts.models import CustomUser
from .models import Organisation

class OrganisationUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Organisation
        fields = ('name', 'email', 'phone', 'email', 
                  'country_code', 'organisation_description',
                  'organisation_logo')

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )    