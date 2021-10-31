# properties/forms.py
from django import forms
from .models import Properties
from django.utils.translation import ugettext_lazy as _
    
# Admin form
class PropertiesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertiesForm, self).__init__(*args, **kwargs)
        self.fields['description'].strip = False

    class Meta:
        model = Properties
        fields = "__all__"

# Property creation form
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
            'property_features',
            'list_date',
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
            "address":_("Address"),
            "number":_("Number"),
            "postalcode":_("Postcode"),
            "geo_lat":_("Latitude"),
            "geo_lng":_("Longitude"),
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
    field_order = ['address','street_number','postalcode','geo_lat', 'geo_lng']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n in self.fields:
            if n == 'photo_main' or n =='photo_1' or n == 'photo_2' or n == 'photo_3' or n == 'photo_4':
                self.fields[n].widget.attrs.update({'class': 'bg-blue-600 rounded-lg text-white shadow'})

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n in self.fields:
            if n == 'photo_main' or n =='photo_1' or n == 'photo_2' or n == 'photo_3' or n == 'photo_4':
                self.fields[n].widget.attrs.update({'class': 'bg-blue-600 rounded-lg text-white shadow'})