# properties/forms
from django import forms
from django.forms import CharField
from .models import Properties


class FilterForm(forms.Form):
    city = CharField(required=True, label=False, widget=forms.TextInput(attrs={'placeholder': 'Postcode, Address, City etc..'}))
    
    
class PropertiesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertiesForm, self).__init__(*args, **kwargs)
        self.fields['description'].strip = False

    class Meta:
        model = Properties
        fields = "__all__"