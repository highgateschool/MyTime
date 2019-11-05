from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path("new", views.TaskCreate.as_view(), name="create_task"),
    path("<int:pk>/edit", views.TaskUpdate.as_view(), name="edit_task"),
    path("<int:pk>/delete", views.TaskDelete.as_view(), name="delete_task")
]
