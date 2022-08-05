from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView)
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate

from .models import User
from .forms import (SigninForm, SignupForm, ChangePasswordForm,
    ResetPasswordForm, PasswordSetForm, ProfileForm)


class SigninView(LoginView):
    template_name = 'signin.html'
    form_class = SigninForm
    redirect_authenticated_user = True


class SignoutView(LogoutView):
    pass


class SignupView(UserPassesTestMixin, CreateView):
    template_name = 'signup.html'
    model = User
    form_class = SignupForm
    success_url = reverse_lazy('users:welcome')

    def test_func(self):
        return self.request.user.is_authenticated == False

    def handle_no_permission(self):
        return redirect(reverse('home'))

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        return response


class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('users:change_password_done')


class ChangePasswordDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'password_change_done.html'


class ResetPasswordView(PasswordResetView):
    template_name = "password_reset_form.html"
    form_class = ResetPasswordForm
    success_url = reverse_lazy("users:password_reset_done")


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = "password_reset_done.html"


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    form_class = PasswordSetForm
    success_url = reverse_lazy("users:password_reset_complete")


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile.html'

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        raise Http404("")
