from django import forms
from catalogue.models import Representation

class RepresentationForm(forms.ModelForm):
    class Meta:
        model = Representation
        fields = ['show', 'schedule', 'location']
        widgets = {
            'schedule': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format d'affichage pour le champ datetime
        if 'schedule' in self.fields:
            self.fields['schedule'].input_formats = ['%Y-%m-%dT%H:%M']
