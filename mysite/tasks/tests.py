import datetime as dt

from django.test import TestCase, Client
from django.utils import timezone

from .models import *
from .scheduler import *
from .statistics import *


class TaskModelTests(TestCase):
    # Test that marking a task as done works as expected
    def test_mark_done_on_todo_task(self):
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
    def test_mark_todo_on_done_task(self):
        # Create a task that is done
        done_task = Task(done=True)
        # Mark it as todo
        done_task.mark_todo()

        # Check the task is not marked as done
        self.assertIs(done_task.done, False)

        # Check that the completion time has been reset
        self.assertEquals(done_task.completion_time, None)

    # Test that the overdue method works correctly
    def test_is_overdue_on_not_overdue_task(self):
        # Create a task that is not overdue
        non_overdue_task = Task(
            due_date=dt.date.today() + dt.timedelta(days=1),
            due_time=dt.time(hour=0, minute=0),
        )

        # Check that the method finds it to not be overdue
        self.assertIs(non_overdue_task.is_overdue(), False)

    def test_is_overdue_on_overdue_task(self):
        # Create a task that is overdue
        overdue_task = Task(
            due_date=dt.date.today() - dt.timedelta(days=1),
            due_time=dt.time(hour=0, minute=0),
        )

        # Check that it is found to be overdue
        self.assertIs(overdue_task.is_overdue(), True)

    # Basic test for time spent alteration
    def test_alter_time_spent(self):
        # Create a taskwith no time spent
        no_time_task = Task()

        # Increase time spent by 10 minutes
        no_time_task.alter_time_spent(dt.timedelta(minutes=10))

        # Check that the time spent is correct
        self.assertEquals(no_time_task.time_spent, dt.timedelta(minutes=10))

    # Test that when altering a task to have negative time spent,
    # it instead is set to 0
    def test_alter_time_spent_negative(self):
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
    def test_same_day_no_time_overlap(self):
        # Define two events which are consecutive but don't overlap
        event_1 = Event(
            date=timezone.now().date(),
            start_time=(timezone.now() - dt.timedelta(minutes=10)).time(),
            end_time=timezone.now().time(),
        )
        event_2 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + dt.timedelta(minutes=10)).time(),
        )

        # Neither should clash with the other
        self.assertIs(event_1.does_clash(event_2), False)
        self.assertIs(event_2.does_clash(event_1), False)

    # Test events where the time overlaps but are on different days
    def test_different_day_overlapping_time(self):
        # Define two events which would clash if they were on the same day,
        # but are on different days
        event_1 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + dt.timedelta(minutes=10)).time(),
        )
        event_2 = Event(
            date=(timezone.now() + dt.timedelta(days=1)).date(),
            start_time=(timezone.now() - dt.timedelta(minutes=5)).time(),
            end_time=(timezone.now() + dt.timedelta(minutes=5)).time(),
        )

        # Neither should clash with the other
        self.assertIs(event_1.does_clash(event_2), False)
        self.assertIs(event_2.does_clash(event_1), False)

    # Test overlapping events
    #
    # Test events overlapping only at one end
    def test_overlap_one_end(self):
        # Define two events which overlap only on one end
        event_1 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + dt.timedelta(minutes=10)).time(),
        )
        event_2 = Event(
            date=timezone.now().date(),
            start_time=(timezone.now() - dt.timedelta(minutes=5)).time(),
            end_time=(timezone.now() + dt.timedelta(minutes=5)).time(),
        )

        # Both should clash with the other
        self.assertIs(event_1.does_clash(event_2), True)
        self.assertIs(event_2.does_clash(event_1), True)

    # Test events overlapping at both ends
    def test_overlap_both_ends(self):
        # Define two events which overlap at both ends
        event_1 = Event(
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + dt.timedelta(minutes=10)).time(),
        )
        event_2 = Event(
            date=timezone.now().date(),
            start_time=(timezone.now() - dt.timedelta(minutes=5)).time(),
            end_time=(timezone.now() + dt.timedelta(minutes=15)).time(),
        )

        # Both should clash with the other
        self.assertIs(event_1.does_clash(event_2), True)
        self.assertIs(event_2.does_clash(event_1), True)


class SchedulerTests(TestCase):
    # Test that the scheduler assigns timeslots for all events and routines on a day
    def test_num_timeslots(self):
        # Specify number of events and routines.
        # These numbers should not be too large so that they can all fit in the one day.
        num_events = 10
        num_routines = 2

        # Create a bunch of events
        for i in range(num_events):
            event = Event(
                date=timezone.now().date(),
                start_time=dt.time(hour=i),
                end_time=dt.time(hour=i, minute=30),
            )
            # They need to be saved to the database so the scheduler can see them
            event.save()

        # Ditto for routines
        for i in range(num_routines):
            routine = Routine(
                day=timezone.now().date().weekday(),
                start_time=dt.time(hour=i + num_events),
                end_time=dt.time(hour=i + num_events, minute=30),
            )
            routine.save()

        # Run the scheduler
        update_schedule(timezone.now().date().weekday())

        # Check that the number of timeslots created is the total no. events and routines
        self.assertEquals(len(TimeSlot.objects.all()), num_events + num_routines)

    # A similar test, this time involving tasks
    def test_num_timeslots_with_tasks(self):
        # Specify number of events, routines and tasks.
        # These numbers should not be too large so that they can all fit in the one day.
        num_events = 10
        num_routines = 2
        num_tasks = 10

        # Create a bunch of events
        for i in range(num_events):
            event = Event(
                date=timezone.now().date(),
                start_time=dt.time(hour=i),
                end_time=dt.time(hour=i, minute=30),
            )
            # They need to be saved to the database so the scheduler can see them
            event.save()

        # Ditto for routines
        for i in range(num_routines):
            routine = Routine(
                day=timezone.now().date().weekday(),
                start_time=dt.time(hour=i + num_events),
                end_time=dt.time(hour=i + num_events, minute=30),
            )
            routine.save()

        # Ditto for tasks
        # I'll create all the tasks with time estimates of 0 so they should definitely be scheduled.
        for i in range(num_tasks):
            task = Task(time_estimate=dt.timedelta(minutes=0))
            task.save()

        # Run the scheduler
        update_schedule(timezone.now().date().weekday())

        # Check that the number of timeslots
        self.assertEquals(
            len(TimeSlot.objects.all()), num_events + num_routines + num_tasks
        )

    # Test that a task which is too long to be scheduled is not scheduled
    def test_unschedulable_task(self):
        # Have the first event of the day from 09:30 to 10:00
        first_event = Event(
            date=timezone.now().date(),
            start_time=dt.time(hour=9, minute=30),
            end_time=dt.time(hour=10),
        )
        first_event.save()

        # Have the last event of the day from 10:30 to 11:00
        last_event = Event(
            date=timezone.now().date(),
            start_time=dt.time(hour=10, minute=30),
            end_time=dt.time(hour=11),
        )
        last_event.save()

        # If the task is longer than 30 minutes, there won't be room to schedule it
        task = Task(time_estimate=dt.timedelta(hours=1))
        task.save()

        # Run the scheduler
        update_schedule(timezone.now().date().weekday())

        # There should only be two timeslots, as the task has not been scheduled
        self.assertEquals(len(TimeSlot.objects.all()), 2)

    # Given the test for no. timeslots with tasks, this is probably redundant,
    # but I'll do it anyway
    def test_schedulable_task(self):
        # Have the first event of the day from 09:30 to 10:00
        first_event = Event(
            date=timezone.now().date(),
            start_time=dt.time(hour=9, minute=30),
            end_time=dt.time(hour=10),
        )
        first_event.save()

        # Have the last event of the day from 10:30 to 11:00
        last_event = Event(
            date=timezone.now().date(),
            start_time=dt.time(hour=10, minute=30),
            end_time=dt.time(hour=11),
        )
        last_event.save()

        # If the task is shorter than 30 minutes, there is room to schedule it
        task = Task(time_estimate=dt.timedelta(minutes=10))
        task.save()

        # Run the scheduler
        update_schedule(timezone.now().date().weekday())

        # There should be three timeslots,
        # for the two events and the task
        self.assertEquals(len(TimeSlot.objects.all()), 3)

    # Test what happens when events have weird timings
    def test_end_before_start_event(self):
        # This event starts at 10:00 and finishes as 09:00
        invalid_event = Event(
            date=timezone.now().date(),
            start_time=dt.time(hour=10),
            end_time=dt.time(hour=9),
        )
        invalid_event.save()

        # Also make a valid event
        valid_event = Event(
            date=timezone.now().date(),
            start_time=dt.time(hour=11),
            end_time=dt.time(hour=12),
        )
        valid_event.save()

        # Run the scheduler
        update_schedule(timezone.now().date().weekday())

        # The scheduler shouldn't create a timeslot for the nonsensical event,
        # so there should only be one timeslot
        self.assertEquals(len(TimeSlot.objects.all()), 1)


class SpecificStatisticsTests(TestCase):
    # Test specific statistics generation
    def test_completion_delta_stats(self):
        # This is just to make sure there are no unexpected small discretions in timings
        time = timezone.now()

        # Test large and small differences between due and completion
        late_one_day = Task(
            done=True,
            due_date=(time - dt.timedelta(days=1)).date(),
            due_time=time.time(),
            completion_time=time,
        )

        early_one_day = Task(
            done=True,
            due_date=time.date(),
            due_time=time.time(),
            completion_time=time + dt.timedelta(days=1),
        )

        late_one_minute = Task(
            done=True,
            due_date=time.date(),
            due_time=(time - dt.timedelta(minutes=1)).time(),
            completion_time=time,
        )

        early_one_minute = Task(
            done=True,
            due_date=time.date(),
            due_time=time.time(),
            completion_time=time + dt.timedelta(minutes=1),
        )

        exactly_due = Task(
            done=True, due_date=time.date(), due_time=time.time(), completion_time=time,
        )

        tasks = [
            late_one_day,
            early_one_day,
            late_one_minute,
            early_one_minute,
            exactly_due,
        ]

        # Run the statistics generator on them
        generate_specific_stats(tasks)

        # Check that the values are what we would expect
        self.assertEquals(late_one_day.completion_delta, dt.timedelta(days=1))
        self.assertEquals(early_one_day.completion_delta, dt.timedelta(days=1))
        self.assertEquals(late_one_minute.completion_delta, dt.timedelta(minutes=1))
        self.assertEquals(early_one_minute.completion_delta, dt.timedelta(minutes=1))

        self.assertEquals(exactly_due.completion_delta, dt.timedelta(minutes=0))

    def test_estimate_accuracy_stats(self):
        # Test large and small differences between time spent and estimated
        second_too_long = Task(
            done=True,
            time_estimate=dt.timedelta(seconds=11),
            time_spent=dt.timedelta(seconds=10),
        )

        second_too_short = Task(
            done=True,
            time_estimate=dt.timedelta(seconds=9),
            time_spent=dt.timedelta(seconds=10),
        )

        hour_too_long = Task(
            done=True,
            time_estimate=dt.timedelta(hours=11),
            time_spent=dt.timedelta(hours=10),
        )

        hour_too_short = Task(
            done=True,
            time_estimate=dt.timedelta(hours=9),
            time_spent=dt.timedelta(hours=10),
        )

        exactly_estimate = Task(
            done=True,
            time_estimate=dt.timedelta(minutes=10),
            time_spent=dt.timedelta(minutes=10),
        )

        tasks = [
            second_too_long,
            second_too_short,
            hour_too_long,
            hour_too_short,
            exactly_estimate,
        ]

        # Run the stats generator
        generate_specific_stats(tasks)

        # Check the values
        self.assertEquals(second_too_long.estimate_accuracy, 10)
        self.assertEquals(second_too_short.estimate_accuracy, 10)
        self.assertEquals(hour_too_long.estimate_accuracy, 10)
        self.assertEquals(hour_too_short.estimate_accuracy, 10)
        self.assertEquals(exactly_estimate.estimate_accuracy, 0)

    # Test null values
    def test_specific_stats_null(self):
        time = timezone.now()

        # Create tasks with unusual attributes
        null_complete = Task(done=True, due_date=time.date(), due_time=time.time(),)

        zero_spent_zero_estimate = Task(done=True)

        zero_spent_nonzero_estimate = Task(
            done=True, time_estimate=dt.timedelta(minutes=10)
        )

        # Run the generator
        generate_specific_stats(
            [null_complete, zero_spent_zero_estimate, zero_spent_nonzero_estimate]
        )

        # Check the stats
        self.assertEquals(null_complete.completion_delta, dt.timedelta(minutes=0))
        self.assertEquals(zero_spent_zero_estimate.estimate_accuracy, 0)
        self.assertEquals(zero_spent_nonzero_estimate.estimate_accuracy, 100)


class GeneralStatisticsTests(TestCase):
    # Create n tasks today and n tasks yesterday
    def setup(self, n):
        # What's the time?
        time = timezone.now()
        yesterday = time - dt.timedelta(days=1)
        # Take precautionary measures
        Task.objects.all().delete()

        # Create a bunch of tasks, done today,
        # in less than estimated time and before their due date
        for i in range(n):
            Task(
                done=True,
                completed_on_time=True,
                completed_in_time=True,
                completion_time=time,
                time_spent=dt.timedelta(minutes=1),
            ).save()

        # Create a bunch of tasks, done yesterday,
        # in over the estimated time and overdue
        for i in range(n):
            Task(
                done=True,
                completed_on_time=False,
                completed_in_time=False,
                completion_time=yesterday,
                time_spent=dt.timedelta(minutes=1),
            ).save()

    def test_num_day(self):
        # Number of tasks
        n = 10
        # Run setup
        self.setup(n)

        # Generate stats
        stats = generate_overall_stats()

        # Check the number today
        self.assertEquals(stats["num day"], n)

    def test_num_week(self):
        # Number of tasks
        n = 10
        # Run setup
        self.setup(n)

        # Generate stats
        stats = generate_overall_stats()

        # Check the number this week
        self.assertEquals(stats["num week"], 2 * n)

    def test_time_day(self):
        # Number of tasks
        n = 10
        # Run setup
        self.setup(n)

        # Generate stats
        stats = generate_overall_stats()

        # Check the time spent today
        self.assertEquals(stats["time day"], timedelta(minutes=n))

    def test_time_week(self):
        # Number of tasks
        n = 10
        # Run setup
        self.setup(n)

        # Generate stats
        stats = generate_overall_stats()

        # Check the time spent this week
        self.assertEquals(stats["time week"], timedelta(minutes=2 * n))

    def test_on_time(self):
        # Number of tasks
        n = 10
        # Run setup
        self.setup(n)

        # Generate stats
        stats = generate_overall_stats()

        # Check the time spent today
        self.assertEquals(stats["on time"], 50)

    def test_in_time(self):
        # Number of tasks
        n = 10
        # Run setup
        self.setup(n)

        # Generate stats
        stats = generate_overall_stats()

        # Check the time spent today
        self.assertEquals(stats["in time"], 50)
