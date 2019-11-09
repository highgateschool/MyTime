from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task


class IndexView(ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'todo_task_list'

    def get_queryset(self):
        return Task.objects.filter(done=False).order_by('-due_date')


class DetailView(DetailView):
    model = Task
    template_name = 'tasks/detail.html'

    def task_done(self):
        Task.mark_done()

    def task_todo(self):
        Task.mark_todo()


class TaskCreate(CreateView):
    model = Task
    fields = ["title", "description", "due_date", "time_estimate"]


# TODO make this change the task instead of creating a new one
class TaskUpdate(UpdateView):
    model = Task
    fields = ["title", "description", "due_date", "time_estimate"]
    template_name = "tasks/task_update_form.html"


# TODO write the HTML for this view, and possibly add relevant code to model
class TaskDelete(DeleteView):
    models = Task
    success_url = reverse_lazy("tasks")


def mark_task_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.mark_done()
    return HttpResponseRedirect(
        reverse("tasks:detail", args=(task.id, )))


def mark_task_todo(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.mark_todo()
    return HttpResponseRedirect(
        reverse("tasks:detail", args=(task.id, )))
