from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from task_manager.settings import LOGIN_URL


class NoPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().id == self.request.user.id

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            'You are not authorized to access this page.',
        )
        self.redirect_url = reverse_lazy('users_list')
        return super().dispatch(request, *args, **kwargs)


class NoPermissionRedirectMixin(object):
    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.redirect_url)


class LoginRequiredRedirectMixin(LoginRequiredMixin):
    """
    A mixin with a custom redirect instead of redirect_to_login().

    A custom redirect is necessary in order to combine this mixin
    with other permission mixins that redirect to different pages.
    """

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.redirect_url)

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            'This option is for registered users only.',
        )
        self.redirect_url = '{login_url}?{next_name}={next_url}'.format(
            login_url=reverse_lazy(LOGIN_URL),
            next_name=REDIRECT_FIELD_NAME,
            next_url=self.request.get_full_path(),
        )
        return super().dispatch(request, *args, **kwargs)
