from django import forms
from django.core.exceptions import ValidationError
import json
from .models import BlogPostPage


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPostPage
        fields = ['title', 'thumbnail',
                  'date_published', 'summary', 'tags', 'body']

    def clean_body(self):
        raw_data = self.data.get('body')
        try:
            # Convert JSON string to Python list
            return json.loads(raw_data)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format for content")
