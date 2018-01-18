from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import QuestionForm, ChoiceForm
from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 5

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.all().order_by('-pub_date')


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

def manage_question(request):
    # empty form if no post data
    form = QuestionForm(request.POST or None)

    ChoiceFormset = modelformset_factory(Choice, form=ChoiceForm)
    queryset = Choice.objects.filter(question=request.question_id)
    formset = ChoiceFormset(request.POST or None, queryset)
    if form.is_valid():
        new_question = form.save(commit=False)
        new_question.pub_date = timezone.now()
        new_question.save()
        return HttpResponseRedirect(reverse('polls:index'))
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'polls/create.html', context)
