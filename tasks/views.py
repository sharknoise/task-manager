from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import View, generic

from task_manager.mixins import (
    LoginRequiredRedirectMixin,
    NoPermissionRedirectMixin,
)
from tasks.models import Task


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class TasksListView(generic.ListView):
    model = Task
    template_name = 'tasks/tasks-list.html'


class TaskCreateView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    SuccessMessageMixin,
    generic.edit.CreateView,
):
    model = Task
    fields = ['name', 'status', 'description', 'executor']
    template_name = 'tasks/task-create.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('You have created a new task!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
