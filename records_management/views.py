from django.shortcuts import render, redirect
from django.db.models import Q #for more sophisticated/realistic queries
from . import models, forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    return render(request, 'records_management/home.html')

def accesslevel_view(request):
    return render(request, 'records_management/access-level-page.html')


#Shows the signup/login for Church Admin
def churchAdminClick_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request, 'records_management/admin_login_signup.html')

#Shows the signup/login page for Church Executive
def churchExecClick_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request, 'records_management/churchexec-click.html')


#shows the credentials-entry page
def churchMemberClick_view(request):
    return render(request, 'records_management/churchmember-click.html')


def churchAdminSignup_view(request):
    if request.method == "POST":
        adminForm = forms.AdminSignupForm(request.POST)
        if adminForm.is_valid():
            user = adminForm.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name="ADMIN")
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('church-admin-login')
    else:
        adminForm = forms.AdminSignupForm()
    return render(request, 'records_management/admin_login_signup.html', {'adminForm': adminForm})


def churchExecSignup_view(request):
    if request.method == 'POST':
        userForm = forms.ExecutiveUserForm(request.POST)
        executiveForm = forms.ExecutiveForm(request.POST, request.FILES)
        if userForm.is_valid() and executiveForm.is_valid():
            exec_user = userForm.save()
            exec_user.set_password(exec_user.password)
            exec_user.save()

            executive = executiveForm.save(commit=False)
            executive.user = exec_user
            executive = executive.save()
            my_executive_group = Group.objects.get_or_create(name='EXECUTIVE / CHURCH LEADER')
            my_executive_group[0].user_set.add(exec_user)

    else:
        userForm = forms.ExecutiveUserForm()
        executiveForm = forms.ExecutiveForm()
    # context = {'userForm': 'userForm', 'executiveForm': 'executiveForm'}
    return render(request, 'records_management/execsignup.html', {'userForm': 'userForm', 'executiveForm': 'executiveForm'})


def member_signup_view(request):
    userForm = forms.ChurchMemberUserForm()
    churchmemberForm = forms.ChurchMemberForm()
    context={'userForm':userForm, 'churchmemberForm':churchmemberForm}
    if request.method == 'POST':
        userForm = forms.ChurchMemberUserForm(request.POST)
        churchmemberForm = forms.ChurchMemberForm(request.POST, request.FILES)
        if userForm.is_valid() and churchmemberForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            churchmember = churchmemberForm.save(commit=False)
            churchmember.user = user
            churchmember = churchmember.save()
            my_churchmember_group = Group.ojects.get_or_create(name='CHURCH MEMBER')
            my_churchmember_group[0].user_set.add(user)
        return HttpResponseRedirect('memberlogin')

    return render(request, 'records_management/churchmember_signup.html', context)




# checks if user is an admin or a church executive
def is_churchadmin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_churchexecutive(user):
    return user.groups.filter(name='EXECUTIVE / CHURCH LEADER').exists()

def is_churchmember(user):
    return user.groups.filter(name='CHURCH MEMBER').exists()


#------- AFTER ENTERING CREDENTIALS, CHECK IF USERNAME & PASSWORD IS THAT OF CHURCH ADMIN OR EXECUTIVE
def afterloginview(request):
    if is_churchadmin(request.user):
        return redirect('churchadmin-dashboard')
    elif is_churchexecutive(request.user):
        accountapproval = models.ChurchLeader.objects.all().filter(user_id=request.user.id, status = True)
        if accountapproval:
            return redirect('church-exec-dashboard')
        else:
            return render(request, 'records_management/exec_await_approval.html')


#<-----------------Views For Church Admin Only----------->
@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def churchadmin_dashboard_view(request):
    leaders = models.ChurchLeader.objects.all().order_by('-id')
    members = models.ChurchMember.objects.all().order_by('-id')
    count_church_members = models.ChurchMember.objects.all().count()
    count_executives = models.ChurchLeader.objects.all().filter().count()
    total_members = count_church_members + count_executives
    context = {
        'leaders':leaders,
        'members':members,
        'count_church_members':count_church_members,
        'count_executives':count_executives,
        'total_members':total_members,
        # 'executive':models.ChurchLeader.objects.get(user_id=request.user.id)
        #for profile picture of admin in the sidebar
    }
    return render(request, 'records_management/admin_dashboard.html', context)


#<-----------------Views For Church Executive/Leader Only----------->
@login_required(login_url='execlogin')
@user_passes_test(is_churchexecutive)
def church_exec_dashboard_view(request):
    #to create three cards 
    count_church_members = models.ChurchMember.objects.all().count()
    count_executives = models.ChurchLeader.objects.all().filter().count()
    total_members = count_church_members + count_executives
    context = {
        'count_church_members':count_church_members,
        'count_executives':count_executives,
        'total_members':total_members,
        'executive':models.ChurchLeader.objects.get(user_id=request.user.id)
        #for profile picture of church executive in the sidebar
    }
    return render(request, 'records_management/exec_dashboard.html', context)


#<----------Views to Search for Church Members--------->
def search_members(request):
    if request.method == "POST":
        searched = request.POST['searched']
        members = models.ChurchMember.objects.filter(member_role=searched)
        context = {
            'searched': searched,
            'members': members
        }
        return render(request, 'RecordsManagement/searchresults_member.html', context)
    else:
        return render(request, 'RecordsManagement/searchresults_member.html')


def list_members(request):
    pass

def show_member(request):
    pass
