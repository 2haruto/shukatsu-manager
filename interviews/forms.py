from django import forms
from .models import ReflectionItem


class ReflectionItemForm(forms.ModelForm):
    class Meta:
        model = ReflectionItem
        fields = ["question", "answer", "improvement"]
        widgets = {
            "question": forms.Textarea(attrs={"rows": 3}),
            "answer": forms.Textarea(attrs={"rows": 3}),
            "improvement": forms.Textarea(attrs={"rows": 3}),
        }
