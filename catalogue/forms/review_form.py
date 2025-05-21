from django import forms
from catalogue.models.review import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        labels = {
            "rating": "Note",
            "comment": "Commentaire",
        }
        widgets = {
            "rating": forms.Select(),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }
