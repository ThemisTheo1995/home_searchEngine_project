# properties/forms.py
from django import forms
from django.forms import CharField
from .models import Properties

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

# Properties creation form     
class PropertiesCreationForm(forms.ModelForm):
    
    class Meta:
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
    # def __init__(self, *args, **kwargs):
    #     super(PropertiesCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['location'].widget.attrs.update({
    #             'id': 'autoComplete',
    #             'placeholder': 'Βρείτε τον Δήμο, Νομό και Χώρα του οικήματος',
    #         })
            
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
        )