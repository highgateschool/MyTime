import datetime
from django import timezone
from .models import Task, Event, Routine


class TimeChunk():
    def __init__(self, obj):
        self.name = obj.get_name()
        self.date = obj.get_day()
        self.start = datetime.combine(date=self.date, time=obj.get_start())
        self.end = datetime.combine(date=self.date, time=obj.get_end())


class AvailableTime(TimeChunk):
    name = "free time"


def make_schedule(day):
    routine = Routine.objects.filter(day=day)[0]
    RoutineTC = TimeChunk(routine)
    date = RoutineTC.date
    events = Event.objects.filter(date=date).order_by("-start_time")

    event_tc_list = []
    for event in events:
        EventTC = TimeChunk(Event)
        event_tc_list.append(EventTC)

    tasks = Task.objects.filter(done=False).order_by("-due_date", "-time_estimate")

