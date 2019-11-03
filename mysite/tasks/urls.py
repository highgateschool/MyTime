from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path("new_task/", views.new_task, name="new_task"),
    path("create_task", views.create_task, name="create_task")
]
