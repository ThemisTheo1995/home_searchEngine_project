# properties/forms
from django import forms
from django.forms import CharField
from .models import Properties


class FilterForm(forms.Form):
    city = CharField(required=True, label=False, widget=forms.TextInput(attrs={'placeholder': 'Postcode, Address, City etc..'}))
    
    
