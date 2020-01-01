from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    due_date = models.DateTimeField('due date')
    time_estimate = models.DurationField('time estimate')
    done = models.BooleanField(default=False)
    override_routine = models.BooleanField(default=False)

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
    purpose = models.CharField(max_length=200, default="event")
    title = models.CharField(max_length=200)
    date = models.DateField("date")
    day = None
    start_time = models.TimeField("start time")
    end_time = models.TimeField("end time")
    override_routine = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_date(self):
        return self.date

    def get_start(self):
        return self.start_time

    def get_end(self):
        return self.end_time

    def get_name(self):
        return self.title

    def does_clash(self, other):
        if self.start_time < other.end_time and self.end_time > other.start:
            return True
        else:
            return False


#class Routine(Event):
#    purpose = models.CharField(max_length=200, default="routine")
#    date = None
#    day = models.IntegerField("day")
#
#    def get_date(self):
#        today = datetime.today()
#        delta = (self.day - today.weekday()) % 7
#        date = datetime.today() + timedelta(days=delta)
#        return date
#
#    def get_day(self):
#        return self.day


class Routine(models.Model):
    day = models.IntegerField("day")
    start_time = models.TimeField("start time")
    end_time = models.TimeField("end time")

    def get_day(self):
        return self.day

    def get_start(self):
        return self.start_time

    def get_end(self):
        return self.end_time


class TimeSlot(models.Model):
    date = models.DateField("date")
    start_time = models.TimeField("start time")
    end_time = models.TimeField("end time")
    associated_object = models.ForeignKey(models.Model,
                                          on_delete=models.CASCADE)

    def get_date(self):
        return self.date

    def get_start(self):
        return self.start_time

    def get_end(self):
        return self.end_time
