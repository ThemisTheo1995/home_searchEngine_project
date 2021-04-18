# realtors/forms
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from .models import Realtor

class RealtorUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Realtor
        fields = ('name', 'email', 'phone', 'email', 
                  'country_code', 'realtor_description',
                  'realtor_logo')