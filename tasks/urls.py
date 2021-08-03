from django.urls import path

from tasks import views

urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
]
