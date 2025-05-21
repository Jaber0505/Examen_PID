from django import forms
from catalogue.models.locality import Locality

class LocalityForm(forms.ModelForm):
    class Meta:
        model = Locality
        fields = ["postal_code", "locality"]
        labels = {
            "postal_code": "Code postal",
            "locality": "Nom de la localité",
        }
        widgets = {
            "postal_code": forms.TextInput(attrs={"placeholder": "Ex : 1000"}),
            "locality": forms.TextInput(attrs={"placeholder": "Ex : Bruxelles"}),
        }
