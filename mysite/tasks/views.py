from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Task

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published questions.
        return Task.objects.order_by('-due_date')


class DetailView(generic.DetailView):
    model = Task
    template_name = 'tasks/detail.html'


def new_task(request):
    task_data = {}
    for item in request.POST:
        try:
            task_data[item] = request.POST[str(item)]
        except KeyError:
            return render(request, 'tasks/add_task.html', {
                'error_message': f'Please enter a valid input for {item}.'
            })
    new_task = Task
    for k, v in task_data:
        setattr(new_task, k, v)
    new_task.save()
    return HttpResponseRedirect(reverse("tasks:index"))
