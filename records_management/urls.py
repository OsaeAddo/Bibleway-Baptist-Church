from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'records_management'

urlpatterns = [
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

    path('afterlogin/', views.afterloginview, name='afterlogin'),

    #<-------------Dashboard Related------------>
    path('churchadmin-dashboard/', views.churchadmin_dashboard_view, name='churchadmin-dashboard'),
    path('church-exec-dashboard/', views.church_exec_dashboard_view, name='church-exec-dashboard'),

    #<------------Search related --------->
    #search church members
    path('search-members/', views.search_members, name='search-members'),
    #list church members
    path('list-members/', views.list_members, name='list-members'),
    #show church member
    path('show-member/', views.show_member, name='show-member'),
]
