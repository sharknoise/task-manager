from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from users.forms import RegistrationForm


class UsersListView(generic.ListView):
    model = get_user_model()
    template_name = 'users/users-list.html'


class RegisterUserView(SuccessMessageMixin, generic.CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = 'users/user-register.html'
    success_url = reverse_lazy('users')
