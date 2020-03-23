#!/usr/bin/env python3

import pytz
from datetime import datetime, timedelta
from itertools import chain
from django.utils import timezone
from .models import Task

# Function to round of time deltas
def chop_microseconds(delta):
    return delta - timedelta(microseconds=delta.microseconds)


# Function for generating the overall statistics
def generate_overall_stats():
    # When this data is received by the view,
    # it will need to put it in the context dictionary,
    # so if we create a dictionary here is will be easy to copy.
    stats = {}

    # Here we'll do some queries to get various lists of tasks we'll need.
    # Note that we're listifying all the queries,
    # as Django provides Q objects,
    # which are a bit different.
    #
    # Tasks completed today:
    tasks_today = list(
        Task.objects.filter(
            done=True,
            completion_time__range=[timezone.now() - timedelta(days=1), timezone.now()],
        )
    )
    # Tasks completed this week:
    tasks_week = list(
        Task.objects.filter(
            done=True,
            completion_time__range=[timezone.now() - timedelta(days=7), timezone.now()],
        )
    )

    # Tasks completed on time:
    tasks_on_time = list(Task.objects.filter(done=True, completed_on_time=True))
    # Tasks completed within their time estimate
    tasks_in_time = list(Task.objects.filter(done=True, completed_in_time=True))

    # All completed tasks
    tasks_done = list(Task.objects.filter(done=True))

    # We simply look at the length of the respective lists,
    # to find out the number of tasks completed in the given timeframe.
    stats["num_day"] = len(tasks_today)
    stats["num_week"] = len(tasks_week)

    # Similarly we can sum the time_spent attributes of the tasks in each list,
    # to get the total time spent
    stats["time_day"] = sum([task.time_spent for task in tasks_today], timedelta())
    stats["time_week"] = sum([task.time_spent for task in tasks_week], timedelta())

    # Here we calculate the percentage, rounded to one decimal place,
    # of tasks completed on time and within their time estimate respectively
    stats["on_time"] = round(100 * len(tasks_on_time) / len(tasks_done), 1)
    stats["in_time"] = round(100 * len(tasks_in_time) / len(tasks_done), 1)

    # And return the dictionary
    return stats


# Function for generating the specific stats for given tasks
def generate_specific_stats(tasks):
    for task in tasks:
        # Create an offset-aware datetime object from the due date and due time,
        # for comparison with the completion datetime
        due = datetime.combine(task.due_date, task.due_time).replace(tzinfo=pytz.UTC)
        complete = task.completion_time

        # This is superflouous but makes the code look nicer
        spent = task.time_spent
        estimate = task.time_estimate

        # Get the difference between completion and due,
        # checking that the task does have a completion time
        if complete:
            task.completion_delta = chop_microseconds(abs(due - complete))
        else:
            task.completion_delta = timedelta(minutes=0)

        # Caculate the estimate accuracy as a percentage, rounded to 1 d.p.
        #
        # Check that time spent is non-zero
        if spent:
            task.estimate_accuracy = round(abs(100 * ((estimate / spent) - 1)), 1)
        # If it's 0, then either the error is 0%, if the estimate was 0,
        # or 100% if the estimate was anything else
        elif estimate == timedelta(minutes=0):
            task.estimate_accuracy = 0
        else:
            task.estimate_accuracy = 100

        task.save()
