from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm)

from .admin import UserCreationForm, UserChangeForm
from .models import User
from utilities.forms import BootstrapMixin


class SigninForm(BootstrapMixin, AuthenticationForm):
    pass


class SignupForm(BootstrapMixin, UserCreationForm):
    pass


class ChangePasswordForm(BootstrapMixin, PasswordChangeForm):
    pass


class ResetPasswordForm(BootstrapMixin, PasswordResetForm):
    pass


class PasswordSetForm(BootstrapMixin, SetPasswordForm):
    pass


class ProfileForm(BootstrapMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'name')
