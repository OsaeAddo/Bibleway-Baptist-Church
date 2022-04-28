from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from recordsManagement import views



urlpatterns = [
    path('', views.home, name='home-page'),
]
