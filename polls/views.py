from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import QuestionForm, ChoiceForm, BaseChoiceFormSet
from .models import Question, Choice, AboutSection

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 5

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class QuestionDelete(generic.edit.DeleteView):
    model = Question
    success_url = reverse_lazy('polls:index')
    template_name = 'polls/confirm_delete.html'


class AboutView(generic.ListView):
    template_name = 'polls/about.html'
    context_object_name = 'about_section_list'

    def get_queryset(self):
        """
        Get all AboutSections and order them by display order.
        """
        return AboutSection.objects.all().order_by('display_order')


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def create_question(request):
    """
    Make a Question by submitting the question title and the text for the Choices in a form.
    """
    # initialise form and formset with post data if possible, otherwise render empty forms
    q_form = QuestionForm(request.POST or None)
    ChoiceFormset = formset_factory(ChoiceForm, formset=BaseChoiceFormSet, extra=0)
    c_formset = ChoiceFormset(request.POST or None)

    if q_form.is_valid() and c_formset.is_valid():
        # make the new question with the pub_date set to now
        new_question = q_form.save(commit=False)
        new_question.author = request.user
        new_question.pub_date = timezone.now()
        new_question.save()
        # make a choice for this question for each filled in choice form
        for choice in c_formset.cleaned_data:
            choice_text = choice.get('choice_text')
            # any unfilled choice has no 'choice_text' key, so ignore these
            if choice_text is not None:
                Choice.objects.create(question=new_question, choice_text=choice_text, votes=0)
        return HttpResponseRedirect(reverse('polls:index'))

    # send the form/formset objects to the template
    context = {
        'q_form': q_form,
        'c_formset': c_formset,
    }
    return render(request, 'polls/create.html', context)


def my_polls(request):
    """
    Show all the polls that the user created.
    If the user is not signed in, redirect to the login screen.
    """
    if request.user.is_authenticated:
        questions = Question.objects.filter(author=request.user)
        context = {'questions': questions}
        return render(request, 'polls/my_polls.html', context)
    else:
        return HttpResponseRedirect(reverse('polls:login')+'?next=/polls/my_polls/')
