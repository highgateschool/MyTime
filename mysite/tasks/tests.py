import datetime as dt

from django.test import TestCase, Client
from django.utils import timezone

from .models import *


class TaskModelTests(TestCase):
    # Test that marking a task as done works as expected
    def mark_done_on_todo_task(self):
        # Create a task that is todo
        todo_task = Task(done=False)
        # Get the time before
        before = timezone.now()
        # Mark task as done
        todo_task.mark_done()
        # Get the time after
        after = timezone.now()

        # Check that the task is indeed marked as done
        self.assertIs(todo_task.done, True)

        # Check that the task was completed between the two timestamps
        not_too_early = bool(todo_task.completion_time >= before)
        not_too_late = bool(todo_task.completion_time <= after)

        self.assertIs(not_too_early, True)
        self.assertIs(not_too_late, True)

    # Test that marking a task as todo works as expected
    def mark_todo_on_done_task(self):
        # Create a task that is done
        done_task = Task(done=True)
        # Mark it as todo
        done_task.mark_todo()

        # Check the task is not marked as done
        self.assertIs(done_task.done, False)

        # Check that the completion time has been reset
        self.assertEquals(done_task.completion_time, None)

    # Test that the overdue method works correctly
    def is_overdue_on_not_overdue_task(self):
        # Create a task that is not overdue
        non_overdue_task = Task(
            due_date=dt.date.today() + dt.timedelta(days=1),
            due_time=dt.time(hour=0, minute=0),
        )

        # Check that the method finds it to not be overdue
        self.assertIs(non_overdue_task.is_overdue(), False)

    def is_overdue_on_overdue_task(self):
        # Create a task that is overdue
        overdue_task = Task(
            due_date=dt.date.today() - dt.timedelta(days=1),
            due_time=dt.time(hour=0, minute=0),
        )

        # Check that it is found to be overdue
        self.assertIs(overdue_task.is_overdue(), True)

    # Basic test for time spent alteration
    def alter_time_spent(self):
        # Create a taskwith no time spent
        no_time_task = Task()

        # Increase time spent by 10 minutes
        no_time_task.alter_time_spent(dt.timedelta(minutes=10))

        # Check that the time spent is correct
        self.assertEquals(no_time_task.time_spent, dt.timedelta(minutes=10))

    # Test that when altering a task to have negative time spent,
    # it instead is set to 0
    def alter_time_spent_negative(self):
        # Create a task with 10 minutes time spent
        ten_minute_task = Task(time_spent=dt.timedelta(minutes=10))

        # Reduce time spent by 20 minutes
        ten_minute_task.alter_time_spent(timedelta(minutes=-20))

        # Time spent should now be 0 minutes, rather then -10
        self.assertEquals(ten_minute_task.time_spent, timedelta(minutes=0))


class EventModelTests(TestCase):
    # Test non-overlapping events
    #
    # Test events that are on the same day and nearly overlap, but don't
    def same_day_no_time_overlap(self):
        # Define two events which are consecutive but don't overlap
        event_1 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time() - dt.timedelta(minutes=10),
            end_time=timezeon.now().time(),
        )
        event_2 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=timezeon.now().time() + dt.timedelta(minutes=10),
        )

        # Neither should clash with the other
        self.assertIs(event_1.does_clash(event_2), False)
        self.assertIs(event_2.does_clash(event_1), False)

    # Test events where the time overlaps but are on different days
    def different_day_overlapping_time(self):
        # Define two events which would clash if they were on the same day,
        # but are on different days
        event_1 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=timezeon.now().time() + dt.timedelta(minutes=10),
        )
        event_2 = Event(
            date=timezone.now().date() + 1,
            start_time=timezone.now().time() - dt.timedelta(minutes=5),
            end_time=timezeon.now().time() + dt.timedelta(minutes=5),
        )

        # Neither should clash with the other
        self.assertIs(event_1.does_clash(event_2), False)
        self.assertIs(event_2.does_clash(event_1), False)

    # Test overlapping events
    #
    # Test events overlapping only at one end
    def overlap_one_end(self):
        # Define two events which overlap only on one end
        event_1 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=timezeon.now().time() + dt.timedelta(minutes=10),
        )
        event_2 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time() - dt.timedelta(minutes=5),
            end_time=timezeon.now().time() + dt.timedelta(minutes=5),
        )

        # Both should clash with the other
        self.assertIs(event_1.does_clash(event_2), False)
        self.assertIs(event_2.does_clash(event_1), False)

    # Test events overlapping at both ends
    def overlap_both_ends(self):
        # Define two events which overlap at both ends
        event_1 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=timezeon.now().time() + dt.timedelta(minutes=10),
        )
        event_2 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time() - dt.timedelta(minutes=5),
            end_time=timezeon.now().time() + dt.timedelta(minutes=15),
        )

        # Both should clash with the other
        self.assertIs(event_1.does_clash(event_2), False)
        self.assertIs(event_2.does_clash(event_1), False)
