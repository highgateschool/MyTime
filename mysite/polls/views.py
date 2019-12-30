from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Question, Choice, Number


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published questions.
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id, )))


def square(request):
    try:
        value = request.POST['input']
        value = int(value)
    except TypeError:
        return render(request, 'polls/thing.html', {
            'error_message': "Please enter an integer."
        })
    except KeyError:
        return render(request, 'polls/thing.html', {
            'error_message': "Invalid input."
        })
    else:
        number = Number(value=value, square=value**2)
        out = f"{number.value} squared is {number.square}"
        number.save()
        return render(request, 'polls/thing.html', {
            'output': out
        })
