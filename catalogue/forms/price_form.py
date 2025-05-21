from django import forms
from catalogue.models.price import Price

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ["type", "price", "start_date", "end_date"]
        labels = {
            "type": "Type de tarif",
            "price": "Montant (€)",
            "start_date": "Début de validité",
            "end_date": "Fin de validité",
        }
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
