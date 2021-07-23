from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect


class NoPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().id == self.request.user.id

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            'You are not authorized to access this page',
        )
        self.redirect_url = reverse_lazy('users_list')
        return super().dispatch(request, *args, **kwargs)


class NoPermissionRedirectMixin(object):
    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.redirect_url)
