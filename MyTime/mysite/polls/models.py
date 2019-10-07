import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Number(models.Model):
    value = models.IntegerField()
    square = models.IntegerField()

    def __str__(self):
        return str(self.value)


class Task(models.Model):
    title = models.CharField(max_length=200)
    descrition = models.CharField(max_length=1000)
    due_date = models.DateField('due date')
    time_estimate = models.IntegerField()
    done = False

    def __str__(self):
        return self.title

    def is_overdue(self):
        return self.due_date < timezone.now()

    def mark_as_done(self):
        self.done = True
