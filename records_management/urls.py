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

    #<-------------SignUp Related----------->
    path('church-admin-signup/', views.churchAdminSignup_view, name='adminsignup'),
    path('church-exec-signup/', views.churchExecSignup_view, name='execsignup'),
    path('church-member-signup/', views.member_signup_view, name='member-signup'),

    #<-------------LogIn Related----------->
    path('church-admin-login/', LoginView.as_view(template_name='RecordsManagement/adminlogin.html'), name='adminlogin'),
    path('church-exec-login/', LoginView.as_view(template_name='RecordsManagement/execlogin.html'), name='execlogin'),
    path('church-member-login/',LoginView.as_view(template_name='RecordsManagement/memberlogin.html'), name='memberlogin'),
]
