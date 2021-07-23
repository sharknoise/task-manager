from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from users.forms import RegistrationForm
from users.mixins import NoPermissionMixin, NoPermissionRedirectMixin


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
    NoPermissionMixin,
    NoPermissionRedirectMixin,
    LoginRequiredMixin,
    generic.DeleteView,
):
    login_url = reverse_lazy('login')
    model = get_user_model()
    template_name = 'users/user-delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _('You have deleted your account.')
