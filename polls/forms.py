from django import forms

from .models import Choice, Question

from . import constants


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(forms.Form):
    choice_text = forms.CharField(max_length=constants.CHOICE_TEXT_LENGTH)