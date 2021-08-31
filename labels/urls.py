from django.urls import path

from labels import views

urlpatterns = [
    path('', views.LabelsListView.as_view(), name='labels_list'),
]
