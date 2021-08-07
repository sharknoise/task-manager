from django.urls import path

from api import views

urlpatterns = [
    path('users/', views.APIUsersListView.as_view(), name='api_users_list'),
    path('tasks/', views.APITasksView.as_view(), name='api_tasks_list'),
]
