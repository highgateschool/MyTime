from django.db import models
from django.utils import timezone
import datetime


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    due_date = models.DateField('due date', default=timezone.now)
    due_time = models.TimeField('due time', default=timezone.now)
    time_estimate = models.DurationField('time estimate',
                                         default=datetime.timedelta(minutes=0))
    priority = models.IntegerField("priority", default=1)
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

<<<<<<< HEAD

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateField("start time")
    finish_time = models.DateField("finish time")
=======
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField("date")
    start_time = models.TimeField("start time")
    end_time = models.TimeField("end time")
    
    def __str__(self):
        return self.title
>>>>>>> origin/ft-scheduler
