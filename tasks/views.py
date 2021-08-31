from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import View, generic

from task_manager.mixins import (
    LoginRequiredRedirectMixin,
    NoPermissionRedirectMixin,
)
from tasks.mixins import IsTaskAuthorMixin
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
    fields = ['name', 'status', 'labels', 'description', 'executor']
    template_name = 'tasks/task-create.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('You have created a new task!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    SuccessMessageMixin,
    generic.edit.UpdateView,
):
    model = Task
    template_name = 'tasks/task-update.html'
    fields = ['name', 'status', 'labels', 'description', 'executor']
    success_message = _('The task has been updated.')
    success_url = reverse_lazy('tasks_list')


class TaskReadView(generic.DetailView):
    model = Task
    template_name = 'tasks/task-read.html'


class TaskDeleteView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    IsTaskAuthorMixin,
    generic.edit.DeleteView,
):
    model = Task
    template_name = 'tasks/task-delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task has been deleted.')

    def delete(self, request, *args, **kwargs):
        """
        Add success message to messages.

        We need this instead of SuccessMessageMixin which
        can't be used with DeleteView.
        """
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
