from django import forms

from .models import Choice, Question

from . import constants


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


class ChoiceForm(forms.Form):
    choice_text = forms.CharField(max_length=constants.CHOICE_TEXT_LENGTH)


class BaseChoiceFormSet(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        """
        The empty_forms and 'extra' forms of Django formsets are automatically set to empty_permitted = True.
        Need to change that here.
        """
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False