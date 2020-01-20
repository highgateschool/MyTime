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

    print("Begin tracing contents of time_slots")

    for item in all_events:
        if isinstance(item, Event):
            print("Appending event...")
            time_slots.append(
                TimeSlot(
                    date=date,
                    start_time=item.get_start(),
                    end_time=item.get_end(),
                    associated_type="E",
                    associated_event=item,
                )
            )
            print(f"Contents: {time_slots}")

        elif isinstance(item, Routine):
            print("Appending routine...")
            time_slots.append(
                TimeSlot(
                    date=date,
                    start_time=item.get_start(),
                    end_time=item.get_end(),
                    associated_type="R",
                    associated_routine=item,
                )
            )
            print(f"Contents: {time_slots}")

        else:
            raise Exception("Looks like we have a problem with creating the TimeSlots.")

        print("Done with adding events/routines.")
        print(f"Contents: {time_slots}")

    pos = 1

    while pos < len(time_slots):
        for task in task_list:
            prev = time_slots[pos - 1]
            curr = time_slots[pos]
            tdelta = datetime.combine(date, curr.get_start()) - datetime.combine(
                date, prev.get_end()
            )
            if tdelta > task.time_estimate:
                start = prev.get_end()
                end = (
                    datetime.combine(date, prev.get_end()) + task.time_estimate
                ).time()
                print("Adding task...")
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
                print(f"Contents: {time_slots}")
                task_list.remove(task)
                if pos < len(time_slots):
                    pos += 1
                    pos += 1

    for item in time_slots:
        item.save()
