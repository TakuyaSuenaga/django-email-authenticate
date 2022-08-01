from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView)
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .forms import SigninForm, SignupForm, ChangePasswordForm


class SigninView(LoginView):
    template_name = 'signin.html'
    form_class = SigninForm
    redirect_authenticated_user = True


class SignoutView(LogoutView):
    pass


class SignupView(CreateView):
    template_name = 'signup.html'
    model = User
    form_class = SignupForm
    success_url = reverse_lazy('users:welcome')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)


class WelcomeView(TemplateView):
    template_name = 'welcome.html'


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('users:change_password_done')


class ChangePasswordDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'password_change_done.html'
