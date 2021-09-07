from django.shortcuts import render, redirect
from django.db.models import Q #for more sophisticated/realistic queries
from . import models, forms
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
def leader_click_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request, 'records_management/churchexec-click.html')


#shows the credentials-entry page
def member_click_view(request):
    return render(request, 'records_management/churchmember-click.html')


def church_admin_signup_view(request):
    if request.method == "POST":
        form = forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name="ADMIN")
            my_admin_group[0].user_set.add(user)
            messages.success(request, "Success: Admin created!")
            return redirect('admin-click')
    else:
        form = forms.AdminSignupForm()
    return render(request, 'records_management/admin_login_signup.html', {'form': form})


def leader_signup_view(request):
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
            my_executive_group = Group.objects.get_or_create(name='LEADERS')
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
            my_churchmember_group = Group.objects.get_or_create(name='MEMBERS')
            my_churchmember_group[0].user_set.add(user)
        return HttpResponseRedirect('memberlogin')

    return render(request, 'records_management/churchmember_signup.html', context)


#To Do later
def customize_churchadmin_login_view(user):
    pass

# checks if user is an admin or a church executive
def is_churchadmin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_churchleader(user):
    return user.groups.filter(name='LEADERS').exists()

def is_churchmember(user):
    return user.groups.filter(name='MEMBERS').exists()


#------- AFTER ENTERING CREDENTIALS, CHECK IF USERNAME & PASSWORD IS THAT OF CHURCH ADMIN OR EXECUTIVE
def afterloginview(request):
    print("-------------afterloginview hit-----------")
    print("******* proceeding to verify if user is admin ******")
    if is_churchadmin(request.user):
        print(f"Admin user is: {request.user}")
        return redirect("churchadmin-dashboard")
    elif is_churchleader(request.user):
        accountapproval = models.ChurchLeader.objects.all().filter(user_id=request.user.id, status = True)
        if accountapproval:
            return redirect('leader-dashboard')
        else:
            return render(request, 'records_management/exec_await_approval.html')


#<-----------------Views For Church Admin Only----------->
@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def churchadmin_dashboard_view(request):
    leaders = models.ChurchLeader.objects.all().order_by('-id')
    count_leaders = models.ChurchLeader.objects.all().filter(status= True).count()
    pending_leaders_count = models.ChurchLeader.objects.all().filter(status=False).count()
    members = models.ChurchMember.objects.all().order_by('-id')
    count_church_members = models.ChurchMember.objects.all().filter(status=True).count()
    pending_members_count = models.ChurchMember.objects.all().filter(status=False).count()
    page = request.GET.get('page', 2)
    paginator = Paginator(members, 2)
    try:
        li_members = paginator.page(page)
    except PageNotAnInteger:
        li_members = paginator.page(1)
    except EmptyPage:
        li_members = paginator.page(paginator.num_pages)
    total_members = count_church_members + count_leaders
    context = {
        'leaders':leaders,
        'count_leaders':count_leaders,
        'pending_leaders_count':pending_leaders_count,
        'members':members,
        'pending_members_count':pending_members_count,
        'count_church_members':count_church_members,
        'li_members': li_members,
        'total_members':total_members,

        # 'executive':models.ChurchLeader.objects.get(user_id=request.user.id)
        #for profile picture of admin in the sidebar
    }
    return render(request, 'records_management/admin_dashboard.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_members_view(request):
    return render(request, 'records_management/admin-member.html')


# List/Table of all members(approved)
@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_list_members_view(request):
    members = models.ChurchMember.objects.all().filter(status=True)
    context = {"members": members}
    return render(request, 'records_management/admin-list-members.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_add_member_view(request):
    userForm = forms.ChurchMemberUserForm()
    memberForm = forms.ChurchMemberForm()
    context = {
        "userForm": userForm,
        "memberForm": memberForm
    }
    if request.method == "POST":
        userForm = forms.ChurchMemberUserForm(request.POST)
        memberForm = forms.ChurchMemberForm(request.POST, request.FILES)
        if userForm.is_valid() and memberForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            member = memberForm.save(commit=False)
            member.user = user
            member.status = True
            member.save()

            member_group = Group.objects.get_or_create(name="MEMBERS")
            member_group[0].user_set.add(user)

        return redirect('admin-list-members')
    return render(request, 'records_management/admin-add-member.html', context)
    


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_delete_member_view(request, pk):
    member = models.ChurchMember.objects.get(id=pk)
    user = models.User.objects.get(id=member.user_id)
    member.delete()
    user.delete()
    return redirect('admin-list-members')


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_update_member_view(request, pk):
    print("************* UPDATE MEMBER HIT ********")
    member = models.ChurchMember.objects.get(id=pk)
    user = models.User.objects.get(id=member.user_id)

    memberForm = forms.ChurchMemberForm(request.FILES, instance=member)
    userForm = forms.ChurchMemberUserForm(instance=user)
    context = {
        'memberForm': memberForm,
        'userForm': userForm
    }
    if request.method == 'POST':
        memberForm = forms.ChurchMemberForm(request.POST, request.FILES, instance=member)
        userForm = forms.ChurchMemberUserForm(request.POST, instance=user)
        if userForm.is_valid() and memberForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            member = memberForm.save(commit=False)
            member.status = True
            member.save()
        return redirect('admin-list-members')

    return render(request, 'records_management/admin-update-member.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_pending_approvals_member_view(request):
    members_pending = models.ChurchMember.objects.all().filter(status=False)
    context = {'members_pending': members_pending}
    return render(request, 'records_management/pending_approvals_member.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_approve_member_view(request, pk):
    members = models.ChurchMember.objects.get(id=pk)
    members.status = True
    members.save()
    return redirect('pending-member')


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def reject_member_view(request, pk):
    member = models.ChurchMember.objects.get(id=pk)
    user = models.User.objects.get(id=member.user_id)
    member.delete()
    user.delete()
    return redirect('pending-member')


#<-----------------Views For Church Executive/Leader Only----------->
@login_required(login_url='execlogin')
@user_passes_test(is_churchleader)
def leader_dashboard_view(request):
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
