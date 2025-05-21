from django import forms
from catalogue.models import ArtistType

class ArtistTypeForm(forms.ModelForm):
    class Meta:
        model = ArtistType
        fields = ['artist', 'type']
        labels = {
            'artist': 'Artiste',
            'type': 'Type',
        }
