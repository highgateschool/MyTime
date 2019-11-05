from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    due_date = models.DateTimeField('due date')
    time_estimate = models.TimeField('time estimate')
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def is_overdue(self):
        return self.due_date < timezone.now()

    def mark_as_done(self):
        self.done = True

    def get_absolute_url(self):
        return f"/tasks/{self.id}/"
