# catalogue/forms/artist_type_show_form.py

from django import forms
from catalogue.models import ArtistTypeShow

class ArtistTypeShowForm(forms.ModelForm):
    class Meta:
        model = ArtistTypeShow
        fields = ['artist_type', 'show']
        labels = {
            'artist_type': 'Artiste + Type',
            'show': 'Spectacle',
        }
