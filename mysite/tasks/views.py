from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task, Event, Routine


class IndexView(ListView):
    template_name = 'tasks/task_index.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.order_by('-due_date')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['todo_tasks'] = Task.objects.filter(
            done=False).order_by("-due_date")
        context['done_tasks'] = Task.objects.filter(
            done=True).order_by("-due_date")
        return context


class DetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

    def task_done(self):
        Task.mark_done()

    def task_todo(self):
        Task.mark_todo()


class TaskCreate(CreateView):
    model = Task
    fields = [
        "title", "description", "due_date", "due_time", "time_estimate",
        "priority"
    ]
    due_date = forms.DateField(widget=forms.SelectDateWidget(
        attrs={'type': 'date'}))
    due_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))


class TaskUpdate(UpdateView):
    model = Task
    fields = [
        "title", "description", "due_date", "due_time", "time_estimate",
        "priority"
    ]
    due_date = forms.DateField(widget=forms.SelectDateWidget(
        attrs={'type': 'date'}))
    due_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    template_name = "tasks/task_update_form.html"


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task_index")


class EventCreate(CreateView):
    model = Event
    fields = ["title", "date", "start_time", "end_time"]
    date = forms.DateField(widget=forms.SelectDateWidget(
        attrs={"type": "date"}))
    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))


class EventUpdate(UpdateView):
    model = Event
    fields = ["title", "date", "start_time", "end_time"]
    date = forms.DateField(widget=forms.SelectDateWidget(
        attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    template_name = "tasks/event_update_form.html"


class EventDelete(DeleteView):
    model = Event
    #success_url = reverse_lazy("tasks:index")


class RoutineCreate(CreateView):
    model = Routine
    fields = ["title", "day", "start_time", "end_time"]
    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))


class RoutineUpdate(UpdateView):
    model = Routine
    fields = ["title", "day", "start_time", "end_time"]
    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    template_name = "tasks/routine_update_form.html"


class RoutineDelete(DeleteView):
    model = Routine
    #success_url = reverse_lazy("tasks:index")


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
