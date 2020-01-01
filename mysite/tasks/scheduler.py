from datetime import datetime, timedelta
from django import timezone
from .models import Task, Event, Routine, TimeChunk


def get_date_from_weekday(day):
    today = datetime.today()
    delta = (day - today.weekday()) % 7
    date = datetime.today() + timedelta(days=delta)
    return date


def clean_task_and_routine_events(date):
    TimeSlot.objects.filter(date=date).delete()


def update_schedule(day):
    date = get_date_from_weekday(day)
    clean_task_and_routine_events(date)

    routines = Routine.objects.filter(day=day)
    events = Event.objects.filter(date=date).order_by("-start_time")
    all_events = (routines + events).order_by("-start_time")
    tasks = Task.objects.filter(done=False).order_by("-due_date",
                                                     "-time_estimate")

    time_slots = []

    for item in all_events:
        if isinstance(item, Event):
            time_slots.append(
                TimeSlot(date=date,
                         start_time=item.get_start(),
                         end_time=item.get_end(),
                         associated_event=item.id))

        elif isinstance(item, Routine):
            time_slots.append(
                TimeSlot(date=date,
                         start_time=item.get_start(),
                         end_time=item.get_end(),
                         associated_routine=item.id))

    pos = 1

    while pos < len(time_slots):
        for task in tasks:
            prev = time_slots[pos - 1]
            curr = time_slote[pos]
            if prev.get_end() - curr.get_start() > task.time_estimate:
                time_slots.insert(
                    i,
                    TimeSlot(date=date,
                             start_time=prev.get_end(),
                             end_time=prev.get_end() + task.time_estimate,
                             associated_task=task.id))
                if pos < len(time_slots):
                    pos += 1
        pos += 1

    for item in time_slots:
        item.save()
