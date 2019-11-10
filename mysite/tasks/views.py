import re
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task


class IndexView(ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'todo_task_list'

    def get_queryset(self):
        #return Task.objects.filter(done=False).order_by('-due_date')
        return Task.objects.order_by('-due_date')


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


class TaskUpdate(UpdateView):
    model = Task
    fields = ["title", "description", "due_date", "time_estimate"]
    template_name = "tasks/task_update_form.html"


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:index")


def mark_task_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    link = request.META.get("HTTP_REFERER", "/")
    task.mark_done()
    task.save()
    return HttpResponseRedirect(link)


def mark_task_todo(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    link = request.META.get("HTTP_REFERER", "/")
    task.mark_todo()
    task.save()
    return HttpResponseRedirect(link)
