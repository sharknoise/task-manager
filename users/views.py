from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model


class UsersListView(generic.ListView):
    model = get_user_model()
    template_name = 'users/users-list.html'
