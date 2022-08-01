from django.urls import path
from .views import *


app_name= 'users'
urlpatterns = [
    path('signin/', SigninView.as_view(), name="signin"),
    path('signout/', SignoutView.as_view(), name="signout"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('welcome/', WelcomeView.as_view(), name="welcome"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('change_password_done/', ChangePasswordDoneView.as_view(), name="change_password_done"),
]
