from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

# app_name = 'records_management'

urlpatterns = [
    path('', views.home, name='home-page'),
    path('access-level/',views.accesslevel_view, name='access-level'),

    #<-------------Click Related----------->
    path('church-leader-click/', views.leader_click_view, name='exec-click'),
    path('church-member-click/', views.member_click_view, name='member-click'),

    #<-------------SignUp Related----------->
    path('church-leader-signup/', views.leader_signup_view, name='leader-signup'),
    path('church-member-signup/', views.member_signup_view, name='member-signup'),

    #<-------------LogIn Related----------->
    path('church-admin-login/', LoginView.as_view(template_name='records_management/admin_login.html'), name='adminlogin'),
    path('church-leader-login/', LoginView.as_view(template_name='records_management/leader_login.html'), name='leader-login'),
    # path('church-member-login/', LoginView.as_view(template_name='records_management/member_login.html'), name='member-login'),

    #<-----AfterLogin Related------>
    path('afterlogin/', views.afterloginview, name='afterlogin'),
    #<--------- Logout Related ------------>
    path('logout/', LogoutView.as_view(template_name='records_management/home.html'), name="admin-logout"),

    #<-------------Dashboard Related------------>
    #-----------Admin Dashboard-----------------
    path('churchadmin-dashboard/', views.churchadmin_dashboard_view, name='churchadmin-dashboard'),
    path('admin-member/', views.admin_members_view, name='admin-member'),
    path('list-members/', views.admin_list_members_view, name='admin-list-members'),
    path('add-member/', views.admin_add_member_view, name='admin-add-member'),
    path('delete-member/<int:pk>', views.admin_delete_member_view, name='admin-delete-member'),
    path('update-member/<int:pk>', views.admin_update_member_view, name='admin-update-member'),
    path('member-pending-approvals/', views.admin_pending_approvals_member_view, name='pending-member'),
    path('approve-member/<int:pk>', views.admin_approve_member_view, name='approve-member'),
    path('reject-member/<int:pk>', views.reject_member_view, name='reject-member'),

    path('admin-leader/', views.admin_leaders_view, name='admin-leader'),
    path('list-leaders/', views.admin_list_leaders_view, name='admin-list-leaders'),
    path('add-leader/', views.admin_add_leader_view, name='admin-add-leader'),
    path('leader-pending-approvals/', views.admin_pending_approvals_leader_view, name='pending-leader'),
    path('approve-leader/<int:pk>', views.admin_approve_leader_view, name='approve-leader'),
    path('reject-leader/<int:pk>', views.reject_leader_view, name='reject-leader'),


    #-----------Leader Dashboard--------------
    path('church-leader-dashboard/', views.leader_dashboard_view, name='leader-dashboard'),

    #<------------Search related --------->
    #search church members
    path('search-members/', views.search_members, name='search-members'),
    #list church members
    path('list-members/', views.list_members, name='list-members'),
    #show church member
    path('show-member/', views.show_member, name='show-member'),
]
