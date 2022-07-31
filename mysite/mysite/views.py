from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class TopPageView(TemplateView):
    template_name = 'toppage.html'


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
