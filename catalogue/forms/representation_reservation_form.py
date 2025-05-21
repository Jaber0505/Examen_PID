from django import forms
from catalogue.models import RepresentationReservation, Price

class RepresentationReservationForm(forms.ModelForm):
    # Champ visuel pour montrer le tarif sans le modifier
    display_price = forms.CharField(label="Tarif", required=False, disabled=True)

    class Meta:
        model = RepresentationReservation
        fields = ['price', 'quantity']
        widgets = {
            'price': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 255})
        }
        labels = {
            'quantity': 'Quantité de places',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        price_obj = self.initial.get("price")

        if isinstance(price_obj, Price):
            self.fields['display_price'].initial = f"{price_obj.type} – {price_obj.price:.2f} €"
            self.fields['price'].initial = price_obj.pk
        elif isinstance(price_obj, int):
            try:
                price = Price.objects.get(pk=price_obj)
                self.fields['display_price'].initial = f"{price.type} – {price.price:.2f} €"
                self.fields['price'].initial = price.pk
            except Price.DoesNotExist:
                self.fields['display_price'].initial = "Tarif introuvable"
        else:
            self.fields['display_price'].initial = "Tarif inconnu"
