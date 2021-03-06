from django.forms import ModelForm, TextInput, Textarea, NumberInput
from django_google_maps import widgets as map_widgets
from estate.models import Condo
import json
from django_google_maps.widgets import GoogleMapsAddressWidget

class CondoForm(ModelForm):
    class Meta:
        model = Condo
        fields = ['name', 'description', 'number_of_floors', 'amenities', 'address', 'geolocation']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': "form-control"}),
            'number_of_floors': NumberInput(attrs={'class': 'form-control'}),
            # 'address': GoogleMapsAddressWidget,
            'address': map_widgets.GoogleMapsAddressWidget(attrs={
                'data-autocomplete-options': json.dumps({
                    'types': ['geocode', 'establishment'],
                    'componentRestrictions': {}
                })
            })
        }
