from django import forms
from catalogue.models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["representation"]
        labels = {
            "representation": "Représentation",
        }
