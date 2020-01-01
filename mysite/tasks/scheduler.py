from datetime import datetime, timedelta
from django import timezone
from .models import Task, Event, Routine, TimeChunk


def make_event_from_task(task, date, task_start):
    task_end = task_start + task.time_estimate
    return Event(purpose="task",
                 title=task.title,
                 date=date,
                 start_time=task_start,
                 end_time=task_end)


def make_event_from_routine(routine, date):
    return Event(purpose="routine",
                 title="routine",
                 date=date,
                 start_time=routine.get_start(),
                 end_time=routine.get_end())


def get_date_from_weekday(day):
    today = datetime.today()
    delta = (day - today.weekday()) % 7
    date = datetime.today() + timedelta(days=delta)
    return date


def clean_task_and_routine_events(date):
    TimeSlot.objects.filter(date=date).delete()


#def split_time_slot(outer, inner):
#    before = TimeSlot(date=outer.get_date(), start_time=outer.get_start(), end_time=inner.get_start())
#    after = TimeSlot(date=outer.get_date(), start_time=inner.get_end(), end_time=outer.get_end())
#    return before, after


def update_schedule(day):
    date = get_date_from_weekday(day)
    clean_task_and_routine_events(date)

    routines = Routine.objects.filter(day=day)
    events = Event.objects.filter(date=date).filter(
        purpose="event").order_by("-start_time")
    all_events = (routines + events).order_by("-start_time")
    tasks = Task.objects.filter(done=False).order_by("-due_date",
                                                     "-time_estimate")

    time_slots = []

    for item in all_events:
        time_slots.append(
            TimeSlot(date=date,
                     start_time=item.get_start(),
                     end_time=item.get_end(),
                     associated_object=item.id))

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
                             associated_object=task.id))
                if pos < len(time_slots):
                    pos += 1
        pos += 1

    for item in time_slots:
        item.save()
