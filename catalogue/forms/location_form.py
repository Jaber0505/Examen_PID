from django import forms
from catalogue.models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            "slug",
            "designation",
            "address",
            "website",
            "phone",
            "locality"
        ]

        labels = {
            "slug": "Identifiant URL",
            "designation": "Nom du lieu",
            "address": "Adresse",
            "website": "Site web",
            "phone": "Téléphone",
            "locality": "Localité"
        }

        help_texts = {
            "slug": "Texte court sans espace pour les URLs (ex: michel-sa)",
            "designation": "Nom complet du lieu (ex: Théâtre Royal)",
            "address": "Adresse complète (ex: rue de Seguin 216)",
            "website": "Lien vers le site (ex: https://...)",
            "phone": "Numéro de téléphone (ex: +32...)",
            "locality": "Choisir une localité existante"
        }
