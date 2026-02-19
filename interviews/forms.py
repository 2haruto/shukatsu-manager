from django import forms
from .models import ReflectionItem, Interview


class ReflectionItemForm(forms.ModelForm):
    class Meta:
        model = ReflectionItem
        fields = ["question", "answer", "improvement"]
        widgets = {
            "question": forms.Textarea(attrs={"rows": 3}),
            "answer": forms.Textarea(attrs={"rows": 3}),
            "improvement": forms.Textarea(attrs={"rows": 3}),
        }


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ["company", "scheduled_at", "stage", "location", "notes", "overall_reflection", "next_action"]
        widgets = {
            "scheduled_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
            "overall_reflection": forms.Textarea(attrs={"rows": 4}),
            "next_action": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["company"].queryset = self.fields["company"].queryset.filter(owner=user)
