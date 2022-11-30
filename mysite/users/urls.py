from django.urls import path
from .views import *


app_name = 'users'
urlpatterns = [
    path(r'signin/', SigninView.as_view(), name="signin"),
    path(r'signout/', SignoutView.as_view(), name="signout"),
    path(r'signup/', SignupView.as_view(), name="signup"),
    path(r'welcome/', WelcomeView.as_view(), name="welcome"),
    path(r'change_password/', ChangePasswordView.as_view(), name="change_password"),
    path(r'change_password_done/', ChangePasswordDoneView.as_view(),
         name="change_password_done"),
    path(r'password_reset/', ResetPasswordView.as_view(), name="password_reset"),
    path(r'password_reset_done/', ResetPasswordDoneView.as_view(),
         name="password_reset_done"),
    path(r'password_reset_confirm/<uidb64>/<token>/',
         ResetPasswordConfirmView.as_view(), name="password_reset_confirm"),
    path(r'password_reset_confirm/', ResetPasswordConfirmView.as_view(),
         name="password_reset_confirm"),
    path(r'password_reset_complete/', ResetPasswordCompleteView.as_view(),
         name="password_reset_complete"),
    path(r'profile/<int:pk>', ProfileView.as_view(), name="profile"),
]
