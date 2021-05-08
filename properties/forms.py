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
        
class PropertiesCreationForm(forms.ModelForm):
    location = forms.CharField(required=True, )
    
    class Meta:
        model = Properties
        exclude = (
            'organisation',
            'property_category',
            'search_address',
            'formatted_address',
            'premise',
            'street_number',
            'route',
            'political',
            'locality',
            'postal_town',
            'neighborhood',
            'administrative_area_level_1',
            'administrative_area_level_2',
            'administrative_area_level_3',
            'administrative_area_level_4',
            'administrative_area_level_5',
            'postalcode',
            'geo_lat',
            'geo_lng',
            'list_date',
            'country',
            'main_type' 
        )
    def __init__(self, *args, **kwargs):
        super(PropertiesCreationForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs.update({
                'id': 'location_search',
                'placeholder': 'Enter address, neighborhood, city, or postal code... 🏡'
            })
            
    field_order = ['location']