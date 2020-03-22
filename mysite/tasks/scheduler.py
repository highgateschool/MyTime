from datetime import datetime, timedelta
from itertools import chain
from django.utils import timezone
from .models import Task, Event, Routine, TimeSlot


# We'll need to be able to figure out a concrete date to place routine events on
# by deriving it from the current date and their assigned weekday
def get_date_from_weekday(day):
    today = datetime.today()
    delta = (day - today.weekday()) % 7
    date = datetime.today() + timedelta(days=delta)
    return date


# When we run the scheduling algorithm, we'll want to clean out any time slots
# from last time
def clean_time_slots(date):
    TimeSlot.objects.filter(date=date).delete()


# Here's the scheduler, it runs based on a given weekday rather than a date.
# This makes things easier
def update_schedule(day):
    # Get the date and clean out time slots
    date = get_date_from_weekday(day)
    clean_time_slots(date)

    # Get all events and routine events for today, ordered by start time
    routines = Routine.objects.filter(day=day).order_by("start_time")
    events = Event.objects.filter(date=date).order_by("start_time")

    # Sort them together
    all_events = sorted(
        chain(routines, events), key=lambda instance: instance.start_time
    )

    # Get all the tasks, ordered by due date, time estimate and descending priority level
    tasks = Task.objects.filter(done=False).order_by(
        "due_date", "time_estimate", "-priority"
    )

    # Convert the iterable into a list, this is easier to handle and we can remove tasks
    # from the list once they have been allocated a time slot
    task_list = list(tasks)

    # Initialise an empty list for holding the time slots, we'll write them all to the
    # database at the end
    time_slots = []

    # Iterate over all the events and routines,
    # creating corresponding time slots
    for item in all_events:
        if isinstance(item, Event):
            ts = TimeSlot(
                date=date,
                start_time=item.get_start(),
                end_time=item.get_end(),
                associated_type="E",
                associated_event=item,
            )

        elif isinstance(item, Routine):
            ts = TimeSlot(
                date=date,
                start_time=item.get_start(),
                end_time=item.get_end(),
                associated_type="R",
                associated_routine=item,
            )

        # Before adding the timslot to the list,
        # check that it has sensible timings.
        # If it doesn't, we can just discard it.
        if ts.start_time <= ts.end_time:
            time_slots.append(ts)

    # We can't use a for loop to iterate through the time slots,
    # because we're going to be changing the length of the list.
    # So we have to use a while loop and a counter to keep track of our position.
    pos = 1

    # Iterate through the time slots
    while pos < len(time_slots):
        # Start by assuming that there is at least one task which will fit in this time gap
        is_room = True

        # As long as tasks keep getting getting inserted,
        # we need to stay here.
        while is_room:
            # Take a note of where we are
            pos_start_loop = pos
            # Iterate over the tasks which are not yet assigned
            for task in task_list:
                # Get the time gap between this timeslot and the last
                prev = time_slots[pos - 1]
                curr = time_slots[pos]
                tdelta = datetime.combine(date, curr.get_start()) - datetime.combine(
                    date, prev.get_end()
                )

                # If the gap is large enought,
                # create a time slot corresponding to the task and put it here
                if tdelta > task.time_estimate:
                    start = prev.get_end()
                    end = (
                        datetime.combine(date, prev.get_end()) + task.time_estimate
                    ).time()
                    time_slots.insert(
                        pos,
                        TimeSlot(
                            date=date,
                            start_time=start,
                            end_time=end,
                            associated_type="T",
                            associated_task=task,
                        ),
                    )

                    task_list.remove(task)

                    # Increment the position,
                    # unless we've reached the end of the list,
                    # in which case there are no more spaces so stop.
                    if pos <= len(time_slots):
                        pos += 1
                    else:
                        break

            # If we reach the end of the loop and the position is the same,
            # that means there's no more room for tasks here,
            # so flag that there is no room and increment position.
            # Otherwise, we go for another loop.
            if pos == pos_start_loop:
                is_room = False
                pos += 1

    # Finally, we save all the time slots to the database
    for item in time_slots:
        item.save()
