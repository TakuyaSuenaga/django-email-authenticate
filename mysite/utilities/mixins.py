from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin


class LogoutRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated is False

    def handle_no_permission(self):
        return redirect(reverse('home'))


class VerifyUserIdentityMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        raise Http404("Access denied.")
