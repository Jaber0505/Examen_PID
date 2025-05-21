from django import forms
from catalogue.models import Artist, Troupe

class ArtistForm(forms.ModelForm):    
    class Meta:
        model = Artist
        fields = ['first_name', 'last_name', 'troupe']
        

class ArtistFormNoTroupe(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['first_name', 'last_name']