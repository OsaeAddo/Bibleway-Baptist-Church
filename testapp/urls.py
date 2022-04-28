from django.urls import path
from django.views.generic import TemplateView

from testapp.views import home_testapp

urlpatterns = [
    path('/', home_testapp)
]