import datetime
from django import timezone
from .models import Task, Event, Routine


class TimeChunk():
    def __init__(self, obj):
        self.date = obj.get_day()
        self.start = datetime.combine(date=self.date, time=obj.get_start())
        self.end = datetime.combine(date=self.date, time=obj.get_end())
