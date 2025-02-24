from django import forms
from .models import Inquiry, Review


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'description', 'linkedin_profile']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['name', 'review', 'positives', 'improvements', 'rating']
