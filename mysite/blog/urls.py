from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path(r'home/', views.HomeView.as_view(), name="home"),
]
