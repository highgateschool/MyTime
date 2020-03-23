from datetime import datetime, timedelta
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Task, Event, Routine, TimeSlot
from .scheduler import *
from .statistics import generate_overall_stats, generate_specific_stats


class IndexView(ListView):
    # Locate the HTML template
    template_name = "tasks/index.html"
    # Name the data for use in the template
    context_object_name = "task_list"

    def get_queryset(self):
        # Get all the tasks
        return Task.objects.order_by("due_date")

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # Get the done and todo tasks separately
        context["todo_tasks"] = Task.objects.filter(done=False).order_by("due_date")
        context["done_tasks"] = Task.objects.filter(done=True).order_by("due_date")
        return context


class StatisticsView(ListView):
    template_name = "tasks/statistics.html"
    context_object_name = "recent_tasks"

    def get_queryset(self):
        # Get 5 most recent completed tasks
        tasks = Task.objects.filter(done=True).order_by("-completion_time")[:5]
        # Run the stats generator for them
        generate_specific_stats(tasks)
        # Return them
        # return tasks
        return Task.objects.filter(done=True).order_by("-completion_time")[:5]

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        # Generate the overall statistics dictionary
        overall_stats = generate_overall_stats()
        # Copy the stats into the context dictionary
        for i in overall_stats:
            context[i] = overall_stats[i]
        return context


class EventView(ListView):
    template_name = "tasks/event_index.html"
    context_object_name = "event_list"

    def get_queryset(self):
        # Get the events in order of their date
        return Event.objects.order_by("date")

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        # Get today's events in time order
        context["events_today"] = Event.objects.filter(date=datetime.today()).order_by(
            "start_time"
        )
        # Likewise for today's routine events
        context["routine_today"] = Routine.objects.filter(
            day=datetime.today().weekday()
        ).order_by("start_time")
        # Likeise for all events and routine events
        context["events"] = Event.objects.order_by("date", "start_time")
        context["routine"] = Routine.objects.order_by("day", "start_time")
        return context


class ScheduleView(ListView):
    template_name = "tasks/schedule.html"
    context_object_name = "time_slots"

    def get_queryset(self):
        # Run the scheduler and get the TimeSlots it creates
        update_schedule(datetime.today().weekday())
        return TimeSlot.objects.filter(date=timezone.now().date()).order_by(
            "start_time"
        )


class TaskDetail(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"

    # Provide a method to mark the task as done
    def task_done(self):
        Task.mark_done()

    # Provide a method to mark the task as todo
    def task_todo(self):
        Task.mark_todo()

    # Provide a method to alter the time
    def task_time_alter(self, mins):
        # Convert the inputted integer to a timedelta of that many minutes
        time_delta = timedelta(minute=mins)
        # Run the task time-alteration method
        Task.alter_time_spent(time_delta)


class EventDetail(DetailView):
    model = Event
    template_name = "tasks/event_detail.html"


class RoutineDetail(DetailView):
    model = Routine
    template_name = "tasks/routine_detail.html"


class TaskCreate(CreateView):
    model = Task

    # The fields the user is allowed to set when creating a task
    fields = [
        "title",
        "description",
        "due_date",
        "due_time",
        "time_estimate",
        "priority",
    ]

    # Provide specialised input for the due date and time
    due_date = forms.DateField(widget=forms.SelectDateWidget(attrs={"type": "date"}))
    due_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))


class EventCreate(CreateView):
    model = Event
    fields = ["title", "date", "start_time", "end_time"]
    date = forms.DateField(widget=forms.SelectDateWidget(attrs={"type": "date"}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))


class RoutineCreate(CreateView):
    model = Routine
    fields = ["title", "day", "start_time", "end_time"]
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))


class TaskUpdate(UpdateView):
    model = Task
    fields = [
        "title",
        "description",
        "due_date",
        "due_time",
        "time_estimate",
        "priority",
    ]
    due_date = forms.DateField(widget=forms.SelectDateWidget(attrs={"type": "date"}))
    due_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    template_name = "tasks/task_update_form.html"


class EventUpdate(UpdateView):
    model = Event
    fields = ["title", "date", "start_time", "end_time"]
    date = forms.DateField(widget=forms.SelectDateWidget(attrs={"type": "date"}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    template_name = "tasks/event_update_form.html"


class RoutineUpdate(UpdateView):
    model = Routine
    fields = ["title", "day", "start_time", "end_time"]
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    template_name = "tasks/routine_update_form.html"


class TaskDelete(DeleteView):
    model = Task
    # Return to the index on a successful completion
    success_url = reverse_lazy("tasks:index")


class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy("tasks:event_index")


class RoutineDelete(DeleteView):
    model = Routine
    success_url = reverse_lazy("tasks:event_index")


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


def change_time_spent(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    link = request.META.get("HTTP_REFERER", "/")
    time = int(request.POST["input"])
    tdelta = timedelta(minutes=time)
    task.alter_time_spent(tdelta)
    task.save()
    return HttpResponseRedirect(link)
