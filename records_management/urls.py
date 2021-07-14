from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'records_management'

url_patterns = [
    path('', views.home, name='home-page'),
    path('access-level/',views.accesslevel_view, name='access-level'),

    #<-------------Click Related----------->
    path('church-admin-click/', views.churchAdminClick_view, name='admin-click'),
    path('church-exec-click/', views.churchExecClick_view, name='exec-click'),
    path('church-member-click/', views.churchMemberClick_view, name='member-click'),
]
