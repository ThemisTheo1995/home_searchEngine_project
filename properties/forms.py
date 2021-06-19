# properties/forms.py
from django import forms
from django.forms import CharField
from .models import Properties
from django.utils.translation import ugettext_lazy as _

class FilterForm(forms.Form):
    city = CharField(required=True, label=False, widget=forms.TextInput(attrs={'placeholder': 'Postcode, Address, City etc..'}))
    
# Admin form
class PropertiesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertiesForm, self).__init__(*args, **kwargs)
        self.fields['description'].strip = False

    class Meta:
        model = Properties
        fields = "__all__"

class PropertiesCreationForm(forms.ModelForm):
    available_after = forms.DateField(
        widget=forms.DateInput(format=('%d-%m-%Y'), 
                               attrs={ 
                               'placeholder':'Select a date',
                               'type':'date',
                               }))
    class Meta:
        # widgets = {
        #     'available_after': DateInput()
        # }
        model = Properties
        exclude = (
            'organisation',
            'property_category',
            'street_number',
            'geo_lat',
            'property_features',
            'geo_lng',
            'list_date',
            'address',
            'identifier',
            'country',
            'country_en',
            'admin_1',
            'admin_1_en',
            'admin_2',
            'admin_2_en',
            'admin_3',
            'admin_3_en',
            'admin_4',
            'admin_4_en',
            'agent',
        )
        labels = {
            "postalcode":_("Postcode"),
            "Property_type": _("Property Type"),
            "advertised": _("Advertised"),
            "description": _("Description"),
            "short_description": _("Short description"),
            "available_after": _("Available after"),
            "currency": _("Currency"),
            "price": _("Price"),
            "bedrooms": _("Bedrooms"),
            "bathrooms": _("Bathrooms"),
            "garage": _("Garage"),
            "furniture": _("Furniture"),
            "m2": _("Square meters (m2)"),
            "photo_main": _("Main photo"),
            "photo_1":_("Photo 1"),
            "photo_2":_("Photo 2"),
            "photo_3":_("Photo 3"),
            "photo_4":_("Photo 4"),
            "is_published":_("Direct publish")
        }         
    field_order = ['postalcode']
    

# Properties update form  
class PropertiesUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Properties
        exclude = (
            'organisation',
            'list_date',
            'country',
            'country_en',
            'admin_1',
            'admin_1_en',
            'admin_2',
            'admin_2_en',
            'admin_3',
            'admin_3_en',
            'admin_4',
            'admin_4_en',
            'identifier',
            'property_features',
        )