from django import forms
from catalogue.models import Price

class MultiTarifReservationForm(forms.Form):
    def __init__(self, *args, available_prices=None, **kwargs):
        super().__init__(*args, **kwargs)

        for price in available_prices:
            field_name = f"quantity_{price.id}"
            self.fields[field_name] = forms.IntegerField(
                label=f"{price.type} – {price.price:.2f} €",
                min_value=0,
                required=False,
                initial=0
            )
