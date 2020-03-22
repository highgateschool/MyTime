import datetime as dt
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone


# class UserData(models.Model):
#    user = models.CharField(max_length=200)
#    tasks_todo = models.IntegerField("tasks todo")
#    tasks_overdue = models.IntegerField("tasks overdue")
#    tasks_done = models.IntegerField("tasks done")
#    tasks_done_recent = models.IntegerField("tasks done recent")
#
#    def find_tasks_todo(self):
#        return len(list(Task.objects.filter_by(associated_user=self, done=False)))
#
#    def find_tasks_overdue(self):
#        return len(
#            list(Task.objects.filter_by(associated_user=self, done=False, overdue=True))
#        )
#
#    def find_tasks_done(self):
#        return len(
#            list(
#                Task.objects.filter_by(associated_user=self, done=True).order_by(
#                    completion_time
#                )[:5]
#            )
#        )
#
#    def find_tasks_done_recent(self):
#        return len(list(Task.objects.filter_by(associated_user=self, done=True)))
#
#    def __str__(self):
#        return f"User data for {self.user}"
#
#    def __repr__(self):
#        return f"User data for {self.user}"


class Task(models.Model):
    # Define the choices to be used in the priority field
    LOW = 1
    MED = 2
    HIGH = 3
    PRIORITY_LIST = [
        (LOW, "Low"),
        (MED, "Normal"),
        (HIGH, "High"),
    ]
    # Define the attributes that tasks will have
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    due_date = models.DateField("due date", default=timezone.now().date())
    due_time = models.TimeField("due time", default=timezone.now().time())
    time_estimate = models.DurationField("time estimate", default=timedelta(minutes=0))
    priority = models.IntegerField("priority", choices=PRIORITY_LIST, default=2)
    done = models.BooleanField(default=False)

    # I realised later that task would additionally need these fields,
    # for the purpose of statistics tracking
    completion_time = models.DateTimeField("completion time", null=True, blank=True)
    completed_on_time = models.BooleanField(default=False)
    completed_in_time = models.BooleanField(default=False)
    time_spent = models.DurationField(
        "time spent", default=timedelta(hours=0, minutes=0)
    )
    completion_delta = models.DurationField("completion delta", null=True, blank=True)
    estimate_accuracy = models.DecimalField(
        "estimate accuracy", max_digits=4, decimal_places=1, null=True, blank=True
    )

    def __str__(self):
        return self.title

    # Check whether the task is overdue
    def is_overdue(self):
        due_datetime = datetime.combine(self.due_date, self.due_time)
        return due_datetime <= datetime.now()

    # Mark the task as done
    def mark_done(self):
        self.done = True

        # At this point we can mark whether the task was completed before it's due date,
        # and within the user's time estimate
        if self.is_overdue():
            self.completed_on_time = False
        else:
            self.completed_on_time = True
        self.completion_time = timezone.now()

        if self.time_spent <= self.time_estimate:
            self.completed_in_time = True
        else:
            self.completed_in_time = False

    # Unmark the task as done
    def mark_todo(self):
        self.done = False
        # These values need to be reset
        self.completed_on_time = False
        self.completed_in_time = False
        self.completion_time = None

    # Alter the time spent on the task
    def alter_time_spent(self, delta):
        # Time spent can't be negative, so need to check
        if (self.time_spent + delta).total_seconds() >= 0:
            self.time_spent += delta
        # If the value would be negative, just set it to 0 minutes
        else:
            self.time_spent = timedelta(minutes=0)

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
        # For events A and B to clash,
        # A must start before B ends and end after B starts
        if (
            self.date == other.date
            and self.start_time < other.end_time
            and self.end_time > other.start_time
        ):
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
    # Define the options to be used in the associated type field
    TYPE_CHOICES = [
        ("T", "task"),
        ("E", "event"),
        ("R", "routine"),
    ]

    # Define the attributes
    date = models.DateField("date")
    start_time = models.TimeField("start time")
    end_time = models.TimeField("end time")

    # Faciltate tracking of the associated object
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
