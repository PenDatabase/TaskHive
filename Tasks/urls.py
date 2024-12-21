from django.urls import path
from . import views



urlpatterns = [
    path('', views.Home, name="home"),
    path('tasks/detail/<slug:slug>', views.TaskDetail.as_view(), name="task-detail"),
    path('tasks/search', views.TaskSearch, name="task_search"),
    path("tasks/categories", views.CategoryList.as_view(), name="job_categories"),
    path("tasks/create", views.CreateTask, name="create_task"),
    path("tasks/update/<slug:slug>", views.UpdateTask, name="update_task"),
    path("tasks/delete/<slug:slug>", views.DeleteTask, name="delete_task")
]
