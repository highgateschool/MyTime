import datetime as dt

from django.test import TestCase, Client
from django.utils import timezone

from .models import *


class TaskModelTests(TestCase):
    def test_mark_done_on_todo_task(self):
        todo_task = Task(done=False)
        todo_task.mark_done()
        self.assertIs(todo_task.done, True)

    def test_mark_todo_on_done_task(self):
        done_task = Task(done=True)
        done_task.mark_todo()
        self.assertIs(done_task.done, False)

    def test_is_overdue_on_not_overdue_task(self):
        non_overdue_task = Task(
            due_date=dt.date.today() + dt.timedelta(days=1),
            due_time=dt.time(hour=0, minute=0),
        )
        self.assertIs(non_overdue_task.is_overdue(), False)
