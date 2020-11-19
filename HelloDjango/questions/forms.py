from django import forms
from .models import Answer, Question


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        exclude = ('pub_date', 'public')


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('title', 'body', 'author')
