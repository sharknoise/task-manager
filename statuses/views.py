from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from statuses.models import Status
from task_manager.mixins import (
    DeletionErrorMixin,
    LoginRequiredRedirectMixin,
    NoPermissionRedirectMixin,
)


class StatusesListView(generic.ListView):
    model = Status
    template_name = 'statuses/statuses-list.html'


class StatusCreateView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    SuccessMessageMixin,
    generic.edit.CreateView,
):
    model = Status
    fields = ['name']
    template_name = 'statuses/status-create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('The status has been created.')

    def form_valid(self, form):
        """
        Add the user to the form as the author of the status.

        We are overriding form_valid() because it is the method
        that eventually returns HttpResponseRedirect().
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class StatusDeleteView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    DeletionErrorMixin,
    generic.edit.DeleteView,
):
    model = Status
    template_name = 'statuses/status-delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('The status has been deleted.')
    error_message = _(
        'Unable to delete the status as it is attached to a task.',
    )


class StatusUpdateView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    SuccessMessageMixin,
    generic.edit.UpdateView,
):
    model = Status
    fields = ['name']
    template_name = 'statuses/status-update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('The status has been updated.')
