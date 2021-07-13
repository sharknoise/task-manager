from django.shortcuts import render
from django.views import View


class UsersListView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/users-list.html')
