from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'industry',
            'website',
            'linkedin',
            'phone',
            'email',
            'city',
            'region',
            'country',
            'status',
            'notes'
        ]
