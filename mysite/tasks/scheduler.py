from datetime import datetime, timedelta
from django import timezone
from .models import Task, Event, Routine, TimeChunk


class TimeSlot():
    def __init__(self, start, end, free):
        self.start = start
        self.end = end
        self.free = free



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


#class AllocatedTimeChunk(TimeChunk): def __init__(self, obj):
#        self.name = obj.get_name()
#        self.date = obj.get_day()
#        self.start = datetime.combine(date=self.date, time=obj.get_start())
#        self.end = datetime.combine(date=self.date, time=obj.get_end())
#
#
#class AvailableTime(TimeChunk):
#    name = "free time"
#
#    def __init__(self, date, start, end):
#        self.date = date
#        self.start = start
#        self.end = end


def get_date_from_weekday(day):
    today = datetime.today()
    delta = (day - today.weekday()) % 7
    date = datetime.today() + timedelta(days=delta)
    return date


def clean_task_and_routine_events(date):
    Event.objects.filter(date=date).exclude(purpose="event").delete()


def update_schedule(day):
    date = get_date_from_weekday(day)
    clean_task_and_routine_events(date)

    routine = Routine.objects.filter(day=day)[0]
    tasks = Task.objects.filter(done=False).order_by("-due_date",
                                                     "-time_estimate")
    events = Event.objects.filter(date=date).filter(purpose="event").order_by("-start_time")

    time_slots = []

    for event in events:
        
