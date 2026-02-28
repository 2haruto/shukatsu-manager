from django import forms
from .models import ReflectionItem, Interview, ExamEvent, StudyLog


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
    scheduled_at = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Interview
        fields = ["company", "scheduled_at", "stage", "location", "notes", "overall_reflection", "next_action"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
            "overall_reflection": forms.Textarea(attrs={"rows": 4}),
            "next_action": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["company"].queryset = self.fields["company"].queryset.filter(owner=user)


class ExamEventForm(forms.ModelForm):
    scheduled_at = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = ExamEvent
        fields = ["school", "title", "event_type", "scheduled_at", "location", "memo"]
        widgets = {
            "memo": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["school"].queryset = self.fields["school"].queryset.filter(owner=user)



class StudyLogForm(forms.ModelForm):
    class Meta:
        model = StudyLog
        fields = [
            "school",
            "subject",
            "title",
            "study_date",
            "duration_minutes",
            "material",
            "content",
            "next_action",
        ]
        widgets = {
            "study_date": forms.DateInput(attrs={"type": "date"}),
            "content": forms.Textarea(attrs={"rows": 4}),
            "next_action": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["school"].queryset = self.fields["school"].queryset.filter(owner=user)
        self.fields["school"].required = False