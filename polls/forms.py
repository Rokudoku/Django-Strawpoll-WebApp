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
    def clean(self):
        """Checks that there are at least 2 forms filled in."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        choice_text_all = []
        for form in self.forms:
            # any empty strings should show up as None
            choice_text = form.cleaned_data.get('choice_text')
            if choice_text is not None:
                choice_text_all.append(choice_text)
        if len(choice_text_all) < 2:
            raise forms.ValidationError("You must have at least 2 choices.")
