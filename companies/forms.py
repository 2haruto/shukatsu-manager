from django import forms
from .models import Company,School


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "role", "status", "priority", "url", "memo"]
        
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            "name",
            "category",
            "school_type",
            "deviation_value",
            "status",
            "exam_date",
            "url",
            "memo",
        ]
        widgets = {
            "exam_date": forms.DateInput(attrs={"type": "date"}),
        }
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "role",
            "status",
            "priority",
            "url",
            "memo",
            "resume_memo",
            "self_pr",
            "motivation",
            "entry_deadline",
            "es_submitted",
            "es_submitted_at",
            "es_version_note",
            "questions_asked",
        ]
        widgets = {
            "memo": forms.Textarea(attrs={"rows": 4}),
            "resume_memo": forms.Textarea(attrs={"rows": 5}),
            "self_pr": forms.Textarea(attrs={"rows": 6}),
            "motivation": forms.Textarea(attrs={"rows": 6}),
            "entry_deadline": forms.DateInput(attrs={"type": "date"}),
            "es_submitted_at": forms.DateInput(attrs={"type": "date"}),
            "es_version_note": forms.Textarea(attrs={"rows": 4}),
            "questions_asked": forms.Textarea(attrs={"rows": 5}),
        }
        
        