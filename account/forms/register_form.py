from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe", "class": "form-input"})
    )
    confirm_password = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmer le mot de passe"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]
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
