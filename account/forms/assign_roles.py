from django import forms
from account.models import Role

class AssignRolesForm(forms.Form):
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Rôles"
    )
