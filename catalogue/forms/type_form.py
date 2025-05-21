from django import forms
from catalogue.models.type import Type

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ["name"]
        labels = {
            "name": "Nom du type",
        }
