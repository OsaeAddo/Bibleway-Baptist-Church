from django.urls import path
from django.views.generic import TemplateView

from testapp import views

urlpatterns = [
    path('', views.HomeTestApp.as_view(), name="home")
]