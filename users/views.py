from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from task_manager.mixins import (
    DeletionErrorMixin,
    LoginRequiredRedirectMixin,
    NoPermissionRedirectMixin,
)
from users.forms import RegistrationForm
from users.mixins import SameUserMixin


class UsersListView(generic.ListView):
    model = get_user_model()
    template_name = 'users/users-list.html'


class RegisterUserView(SuccessMessageMixin, generic.CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = 'users/user-register.html'
    success_url = reverse_lazy('login')
    success_message = _('You have successfully registered!')


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'users/user-login.html'
    success_message = _('You are logged in.')


class LogoutUserView(SuccessMessageMixin, LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _('You have logged out.'))
        # LogoutView.dispatch() is the method that calls auth_logout()
        return super().dispatch(request, *args, **kwargs)


class DeleteUserView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    SameUserMixin,
    SuccessMessageMixin,
    DeletionErrorMixin,
    generic.DeleteView,
):
    model = get_user_model()
    template_name = 'users/user-delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _('You have deleted your account.')
    error_message = _(
        'Unable to delete the account: this user has a task assigned.',
    )


class UpdateUserView(
    NoPermissionRedirectMixin,
    LoginRequiredRedirectMixin,
    SameUserMixin,
    SuccessMessageMixin,
    generic.edit.UpdateView,
):
    model = get_user_model()
    template_name = 'users/user-update.html'
    form_class = RegistrationForm
    success_message = _('Your profile has been updated.')
    success_url = reverse_lazy('users_list')
