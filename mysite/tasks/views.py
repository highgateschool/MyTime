from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task


class IndexView(ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'todo_task_list'

    # TODO filter by tasks which aren't done
    def get_queryset(self):
        return Task.objects.order_by('-due_date')


class DetailView(DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class TaskCreate(CreateView):
    model = Task
    fields = ["title", "description", "due_date", "time_estimate"]


# TODO make this change the task instead of creating a new one
class TaskUpdate(UpdateView):
    model = Task
    fields = ["title", "description", "due_date", "time_estimate"]


# TODO write the HTML for this view, and possibly add relevant code to model
class TaskDelete(DeleteView):
    models = Task
    success_url = reverse_lazy("tasks")
