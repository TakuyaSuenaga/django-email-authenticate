from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .admin import UserCreationForm
from utilities.forms import BootstrapMixin


class SigninForm(BootstrapMixin, AuthenticationForm):
    pass


class SignupForm(BootstrapMixin, UserCreationForm):
    pass


class ChangePasswordForm(BootstrapMixin, PasswordChangeForm):
    pass


