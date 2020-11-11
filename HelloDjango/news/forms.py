from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Форма комменатриев"""
    class Meta:
        model = Review
        exclude = ('pub_date', 'public')
