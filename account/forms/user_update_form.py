from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            "username": "Nom d'utilisateur",
            "email": "Adresse e-mail",
            "first_name": "Prénom",
            "last_name": "Nom",
        }
        help_texts = {
            "username": "",  # Supprimer "Required. 150 characters..."
            "email": "",
        }
