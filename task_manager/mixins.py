from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import DeletionMixin

from task_manager.settings import LOGIN_URL


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


class DeletionErrorMixin(DeletionMixin):
    success_url = reverse_lazy('home')
    success_message = _('The object has been deleted.')
    error_message = _(
        'Unable to delete: the object is used by another object.',
    )

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return response
        except ProtectedError:
            messages.error(request, self.error_message)
            return HttpResponseRedirect(self.success_url)
