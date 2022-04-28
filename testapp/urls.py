from django.urls import path
from django.views.generic import TemplateView

from testapp import views

urlpatterns = [
    path('', views.home_testapp, name="home")
]