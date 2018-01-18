from django.forms import ModelForm, Textarea

from .models import Choice, Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']