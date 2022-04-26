from django.urls import path

from recordsManagement import views

urlpatterns = [
    path('', views.home, name="home")
]