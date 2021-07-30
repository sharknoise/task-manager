from django.urls import path

from statuses import views

urlpatterns = [
    path('', views.StatusesListView.as_view(), name='statuses'),
]
