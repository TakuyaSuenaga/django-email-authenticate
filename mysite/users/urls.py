from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path(r'signin/', views.SigninView.as_view(), name="signin"),
    path(r'signout/', views.SignoutView.as_view(), name="signout"),
    path(r'signup/', views.SignupView.as_view(), name="signup"),
    path(r'welcome/', views.WelcomeView.as_view(), name="welcome"),
    path(r'change_password/', views.ChangePasswordView.as_view(),
         name="change_password"),
    path(r'change_password_done/', views.ChangePasswordDoneView.as_view(),
         name="change_password_done"),
    path(r'password_reset/', views.ResetPasswordView.as_view(),
         name="password_reset"),
    path(r'password_reset_done/', views.ResetPasswordDoneView.as_view(),
         name="password_reset_done"),
    path(r'password_reset_confirm/<uidb64>/<token>/',
         views.ResetPasswordConfirmView.as_view(),
         name="password_reset_confirm"),
    path(r'password_reset_confirm/', views.ResetPasswordConfirmView.as_view(),
         name="password_reset_confirm"),
    path(r'password_reset_complete/',
         views.ResetPasswordCompleteView.as_view(),
         name="password_reset_complete"),
    path(r'profile/<int:pk>', views.ProfileView.as_view(),
         name="profile"),
]
