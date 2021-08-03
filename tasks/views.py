from django.shortcuts import render
from django.views import View, generic

from tasks.models import Task


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class TasksListView(generic.ListView):
    model = Task
    template_name = 'tasks/tasks-list.html'
