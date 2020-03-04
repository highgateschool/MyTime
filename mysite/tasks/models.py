import datetime as dt
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone


class UserData(models.Model):
    user = models.CharField(max_length=200)
    tasks_todo = models.IntegerField("tasks todo")
    tasks_overdue = models.IntegerField("tasks overdue")
    tasks_done = models.IntegerField("tasks done")
    tasks_done_recent = models.IntegerField("tasks done recent")

    def find_tasks_todo(self):
        pass

    def __str__(self):
        return f"User data for {user}"

    def __repr__(self):
        return f"User data for {user}"


class Task(models.Model):
    LOW = 1
    MED = 2
    HIGH = 3
    PRIORITY_LIST = [
        (LOW, "Low"),
        (MED, "Normal"),
        (HIGH, "High"),
    ]
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    due_date = models.DateField("due date", default=timezone.now().date())
    due_time = models.TimeField("due time", default=timezone.now().time())
    time_estimate = models.DurationField("time estimate")
    priority = models.IntegerField("priority", choices=PRIORITY_LIST, default=2)
    done = models.BooleanField(default=False)
    completed_on_time = models.BooleanField(default=False)
    time_spent = models.DurationField(
        "time spent", default=timedelta(hours=0, minutes=0)
    )
    associated_user = models.ForeignKey(UserData, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def is_overdue(self):
        due_datetime = datetime.combine(self.due_date, self.due_time)
        return due_datetime <= datetime.now()

    def mark_done(self):
        self.done = True
        if self.is_overdue():
            self.completed_on_time = False
        else:
            self.completed_on_time = True

    def mark_todo(self):
        self.done = False

    def get_absolute_url(self):
        return f"/task/{self.id}/"


class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField("date")
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

    def get_absolute_url(self):
        return f"/event/{self.id}/"


class Routine(models.Model):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6
    DAY_CHOICES = [
        (MON, "Monday"),
        (TUE, "Tuesday"),
        (WED, "Wednesday"),
        (THU, "Thursday"),
        (FRI, "Friday"),
        (SAT, "Saturday"),
        (SUN, "Sunday"),
    ]

    title = models.CharField(max_length=200, null=True)
    day = models.IntegerField("day", choices=DAY_CHOICES)
    start_time = models.TimeField("start time")
    end_time = models.TimeField("end time")

    def get_day(self):
        return self.day

    def get_start(self):
        return self.start_time

    def get_end(self):
        return self.end_time

    def get_absolute_url(self):
        return f"/routine/{self.id}/"


class TimeSlot(models.Model):
    TYPE_CHOICES = [
        ("T", "task"),
        ("E", "event"),
        ("R", "routine"),
    ]

    date = models.DateField("date")
    start_time = models.TimeField("start time")
    end_time = models.TimeField("end time")
    associated_type = models.CharField("type", max_length=200, choices=TYPE_CHOICES)
    associated_task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    associated_event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    associated_routine = models.ForeignKey(Routine, on_delete=models.CASCADE, null=True)

    def get_date(self):
        return self.date

    def get_start(self):
        return self.start_time

    def get_end(self):
        return self.end_time

    def __str__(self):
        return f"TimeSlot type {self.associated_type}"

    def __repr__(self):
        return f"TimeSlot type {self.associated_type}"
