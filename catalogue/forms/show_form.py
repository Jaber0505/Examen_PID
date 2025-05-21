from django import forms
from catalogue.models.show import Show

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = [
            "title",
            "description",
            "poster_url",
            "duration",
            "created_in",
            "location",
            "bookable"
        ]
        labels = {
            "title": "Titre",
            "description": "Description",
            "poster_url": "Affiche (URL)",
            "duration": "Durée (en minutes)",
            "created_in": "Année de création",
            "location": "Lieu",
            "bookable": "Réservable"
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
