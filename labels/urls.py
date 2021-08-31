from django.urls import path

from labels import views

urlpatterns = [
    path('', views.LabelsListView.as_view(), name='labels_list'),
    path('create/', views.LabelCreateView.as_view(), name='label_create'),
    path(
        '<int:pk>/delete/',
        views.LabelDeleteView.as_view(),
        name='label_delete',
    ),
    path(
        '<int:pk>/update/',
        views.LabelUpdateView.as_view(),
        name='label_update',
    ),
]
