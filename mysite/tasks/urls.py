from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path("tasks/", views.IndexView.as_view(), name="index"),
    path("events/", views.EventView.as_view(), name="event_index"),
    path("schedule/", views.ScheduleView.as_view(), name="schedule"),
    path("task/<int:pk>/", views.TaskDetail.as_view(), name="task_detail"),
    path("new_task/", views.TaskCreate.as_view(), name="create_task"),
    path("task/<int:pk>/edit/", views.TaskUpdate.as_view(), name="edit_task"),
    path("task/<int:pk>/delete/", views.TaskDelete.as_view(), name="delete_task"),
    path("task/<int:task_id>/mark_done/", views.mark_task_done, name="mark_as_done"),
    path("task/<int:task_id>/mark_todo/", views.mark_task_todo, name="mark_as_todo"),
    path(
        "task/<int:task_id>/change_time_spent/",
        views.change_time_spent,
        name="change_time_spent",
    ),
    path("event/<int:pk>/", views.EventDetail.as_view(), name="event_detail"),
    path("new_event/", views.EventCreate.as_view(), name="create_event"),
    path("event/<int:pk>/edit/", views.EventUpdate.as_view(), name="edit_event"),
    path("event/<int:pk>/delete/", views.EventDelete.as_view(), name="delete_event"),
    path("routine/<int:pk>/", views.RoutineDetail.as_view(), name="routine_detail"),
    path("new_routine/", views.RoutineCreate.as_view(), name="create_routine"),
    path("routine/<int:pk>/edit/", views.RoutineUpdate.as_view(), name="edit_routine"),
    path(
        "routine/<int:pk>/delete/", views.RoutineDelete.as_view(), name="delete_routine"
    ),
    path("stats/", views.StatisticsView.as_view(), name="user_statistics"),
]
