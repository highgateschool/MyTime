from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path('', views.IndexView.as_view(), name='task_index'),
    path('task/<int:pk>/', views.DetailView.as_view(), name='task_detail'),
    path("new_task/", views.TaskCreate.as_view(), name="create_task"),
    path("/task/<int:pk>/edit/", views.TaskUpdate.as_view(), name="edit_task"),
    path("/task/<int:pk>/delete/",
         views.TaskDelete.as_view(),
         name="delete_task"),
    path("/task/<int:task_id>/mark_done/",
         views.mark_task_done,
         name="mark_as_done"),
    path("/task/<int:task_id>/mark_todo/",
         views.mark_task_todo,
         name="mark_as_todo"),
    path("new_event/", views.EventCreate.as_view(), name="create_event"),
    path("/event/<int:pk>/edit/",
         views.EventUpdate.as_view(),
         name="edit_event"),
    path("/event/<int:pk>/delete/",
         views.EventDelete.as_view(),
         name="delete_event"),
    path("new_routine/", views.RoutineCreate.as_view(), name="create_routine"),
    path("/routine/<int:pk>/edit/",
         views.RoutineUpdate.as_view(),
         name="edit_routine"),
    path("/routine/<int:pk>/delete/",
         views.RoutineDelete.as_view(),
         name="delete_routine"),
]
