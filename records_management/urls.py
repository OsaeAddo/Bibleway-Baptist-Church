from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'records_management'

url_patterns = [
    path('', views.home, name='home-page'),
    path('access-level/',views.accesslevel_view, name='access-level'),
]