from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from labels.models import Label
from task_manager.mixins import (
    DeletionErrorMixin,
    LoginRequiredRedirectMixin,
    NoPermissionRedirectMixin,
)


class LabelsListView(generic.ListView):
    model = Label
    template_name = 'labels/labels-list.html'


class LabelCreateView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    SuccessMessageMixin,
    generic.edit.CreateView,
):
    model = Label
    fields = ['name', 'description']
    template_name = 'labels/label-create.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('The label has been created.')

    def form_valid(self, form):
        """
        Add the user to the form as the author of the label.

        We are overriding form_valid() because it is the method
        that eventually returns HttpResponseRedirect().
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelDeleteView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    DeletionErrorMixin,
    generic.edit.DeleteView,
):
    model = Label
    template_name = 'labels/label-delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('The label has been deleted.')
    error_message = _(
        'Unable to delete the label as it is attached to a task.',
    )


class LabelUpdateView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    SuccessMessageMixin,
    generic.edit.UpdateView,
):
    model = Label
    fields = ['name', 'description']
    template_name = 'labels/label-update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('The label has been updated.')
