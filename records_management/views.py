from django.shortcuts import render, redirect
from . import models, forms
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    return render(request, 'records_management/home.html')

def accesslevel_view(request):
    return render(request, 'records_management/access-level-page.html')


#Shows the signup/login page for Church leader
def leader_click_view(request):
    # if request.user.is_authenticated:
    #     return redirect('afterlogin')
    return render(request, 'records_management/church-leader-click.html')


#shows the credentials-entry page
def member_click_view(request):
    return render(request, 'records_management/churchmember-click.html')


def leader_signup_view(request):
    userForm = forms.LeaderUserForm()
    leaderForm = forms.LeaderForm()
    context = {
        'userForm': userForm, 
        'leaderForm': leaderForm
    }
    if request.method == 'POST':
        userForm = forms.LeaderUserForm(request.POST)
        leaderForm = forms.LeaderForm(request.POST, request.FILES)
        if userForm.is_valid() and leaderForm.is_valid():
            leader_user = userForm.save()
            leader_user.set_password(leader_user.password)
            leader_user.save()

            leader = leaderForm.save(commit=False)
            leader.user = leader_user
            leader = leader.save()
            my_leader_group = Group.objects.get_or_create(name='LEADERS')
            my_leader_group[0].user_set.add(leader_user)
    return render(request, 'records_management/leader_signup.html', context)


def member_signup_view(request):
    userForm = forms.ChurchMemberUserForm()
    churchmemberForm = forms.ChurchMemberForm()
    context={
        'userForm':userForm, 
        'churchmemberForm':churchmemberForm
    }
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
        return redirect('member-login')

    return render(request, 'records_management/churchmember_signup.html', context)


#To Do later
def customize_churchadmin_login_view(user):
    pass

# checks if user is an admin or a church leader
def is_churchadmin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_churchleader(user):
    return user.groups.filter(name='LEADERS').exists()

def is_churchmember(user):
    return user.groups.filter(name='MEMBERS').exists()


#------- AFTER ENTERING CREDENTIALS, CHECK IF USERNAME & PASSWORD IS THAT OF CHURCH ADMIN OR leader
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
    else:
        return render(request, 'records_management/unknown-user.html')


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
    paginator_member = Paginator(members, 3)
    page = request.GET.get('page', 2)
    try:
        li_members = paginator_member.page(page)
    except EmptyPage:
        li_members = paginator_member.page(paginator_member.num_pages)
    except PageNotAnInteger:
        li_members = paginator_member.page(1)

    paginator_leader = Paginator(leaders, 3)
    try:
        li_leaders = paginator_leader.page(page)
    except EmptyPage:
        li_leaders = paginator_leader.page(paginator_leader.num_pages)
    except PageNotAnInteger:
        li_leaders = paginator_leader.page(1)
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
        messages.success(request, "Success: New Church Member Added!")
        return redirect('admin-list-members')
    return render(request, 'records_management/admin-add-member.html', context)
    


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_delete_member_view(request, pk):
    member = models.ChurchMember.objects.get(id=pk)
    user = models.User.objects.get(id=member.user_id)
    messages.warning(request, "This action is irreversible!")
    member.delete()
    user.delete()
    messages.success(request, "Success: Church Member Deleted!")
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
        messages.success(request, "Success: Church Member Updated!")
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


# <------Admin Leaders Section ------>
@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_leaders_view(request):
    return render(request, 'records_management/admin-leader.html')


# List/Table of all members(approved)
@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_list_leaders_view(request):
    leaders = models.ChurchLeader.objects.all().filter(status=True)
    context = {"leaders": leaders}
    return render(request, 'records_management/admin-list-leaders.html', context)


#<-----------------Views For Church Leader Only----------->
@login_required(login_url='execlogin')
@user_passes_test(is_churchleader)
def leader_dashboard_view(request):
    #to create three cards 
    count_church_members = models.ChurchMember.objects.all().count()
    count_leaders = models.ChurchLeader.objects.all().filter().count()
    total_members = count_church_members + count_leaders
    context = {
        'count_church_members':count_church_members,
        'count_leaders':count_leaders,
        'total_members':total_members,
        'leader':models.ChurchLeader.objects.get(user_id=request.user.id)
        #for profile picture of church leader in the sidebar
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
