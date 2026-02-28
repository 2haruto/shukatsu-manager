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