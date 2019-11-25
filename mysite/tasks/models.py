from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    due_date = models.DateTimeField('due date')
    time_estimate = models.DurationField('time estimate')
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def is_overdue(self):
        return self.due_date < timezone.now()

    def mark_done(self):
        self.done = True

    def mark_todo(self):
        self.done = False

    def get_absolute_url(self):
        return f"/tasks/{self.id}/"

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField("date")
    start_time = models.TimeField("start time")
    end_time = models.TimeField("end time")
    
    def __str__(self):
        return self.title
