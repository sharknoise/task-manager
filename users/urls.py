from django.urls import path

from users import views


urlpatterns = [
    path('', views.UsersListView.as_view(), name='users_list'),
]