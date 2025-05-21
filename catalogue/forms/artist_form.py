from django import forms
from catalogue.models import Artist, Troupe

class ArtistForm(forms.ModelForm):
    troupe = forms.ModelChoiceField(
        queryset=Troupe.objects.all(),
        required=False,
        empty_label="<< Non affilié >>"
    )

    class Meta:
        model = Artist
        fields = ['first_name', 'last_name', 'troupe']

class ArtistTroupeForm(forms.ModelForm):
    troupe = forms.ModelChoiceField(
        queryset=Troupe.objects.all(),
        required=False,
        empty_label="Non affilié",
        label="Troupe"
    )

    class Meta:
        model = Artist
        fields = ['troupe']