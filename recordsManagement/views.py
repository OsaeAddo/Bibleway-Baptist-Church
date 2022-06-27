from . import models, forms


from django.db.models import Q
from django.views.generic.list import ListView


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from twilio.rest import Client

account_sid = "ACf7c91b1069ec15b5e13eac3f20cd7862"
auth_token = "3d287ad897acc2ac320af07f43d26f36"
client = Client(account_sid, auth_token)
sender = '+19403405520'
recipient = '+233550125552'



# Create your views here.
def home(request):
    return render(request, 'recordsManagement/home.html')

def accesslevel_view(request):
    return render(request, 'recordsManagement/access-level-page.html')


#Shows the signup/login page for Church leader
def leader_click_view(request):
    # if request.user.is_authenticated:
    #     return redirect('afterlogin')
    return render(request, 'recordsManagement/church-leader-click.html')


#shows the credentials-entry page
def member_click_view(request):
    return render(request, 'recordsManagement/churchmember-click.html')


def leader_signup_view(request):
    
    if request.method == 'POST':
        userForm = forms.LeaderUserForm(request.POST)
        leaderForm = forms.LeaderForm(request.POST, request.FILES)
        print(f"**** Valid leaderForm: {leaderForm.is_valid()} ****")
        print(f"**** Valid userForm: {userForm.is_valid()} ****")
        print(f"**** UserForm errors: {userForm.errors.as_data()} ****")
        print(f"**** LeaderForm errors: {leaderForm.errors.as_data()} ****")
        if userForm.is_valid() and leaderForm.is_valid():
            print("******* Valid Leader Forms ******")
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            leader = leaderForm.save(commit=False)
            leader.user = user
            leader = leader.save()
            print("**** Leader Forms saved! ******")
            my_leader_group = Group.objects.get_or_create(name='LEADERS')
            my_leader_group[0].user_set.add(user)
            print("****  Leader added to Group!  ****")
            
        # send sms when a leader signs up
        message = client.messages \
                        .create(
                            body = "Hello admin, a church leader account was just initiated on the website of Bibleway Baptist Church! Kindly verify & approve.",
                            from_=sender,
                            to=recipient
                        )
        print("***** Before redirecting ******")
        return redirect('leader-login')
    
    else:
        userForm = forms.LeaderUserForm()
        leaderForm = forms.LeaderForm()
        
    context = {
        'userForm': userForm, 
        'leaderForm': leaderForm
    }
    return render(request, 'recordsManagement/leader_signup.html', context)


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
            print("******* Valid Member Forms ******")

            user = userForm.save()
            user.set_password(user.password)
            user.save()

            churchmember = churchmemberForm.save(commit=False)
            churchmember.user = user
            churchmember = churchmember.save()
            my_churchmember_group = Group.objects.get_or_create(name='MEMBERS')
            my_churchmember_group[0].user_set.add(user)
        return redirect('home-page')

        # send sms when a member signs up
        message = client.messages \
                        .create(
                            body = "Hello admin, a church member account was just initiated on the website of Bibleway Baptist Church! Kindly verify & approve.",
                            from_=sender,
                            to=recipient
                        )
    return render(request, 'recordsManagement/churchmember_signup.html', context)


#To Do later
def customize_churchadmin_login_view(user):
    pass

# checks if user is an admin or a church leader
def is_churchadmin(user):
    return user.groups.filter(name='ADMINS').exists()

def is_churchleader(user):
    return user.groups.filter(name='LEADERS').exists()

def is_churchmember(user):
    return user.groups.filter(name='MEMBERS').exists()


#------- AFTER ENTERING CREDENTIALS, CHECK IF USERNAME & PASSWORD IS THAT OF CHURCH ADMIN OR leader
def afterloginview(request):
    print("-------------afterloginview hit-----------")
    print("******* proceeding to verify if user is authorized ******")
    if is_churchadmin(request.user):
        return redirect("churchadmin-dashboard")
    elif is_churchleader(request.user):
        accountapproval = models.ChurchLeader.objects.all().filter(user_id=request.user.id, status = True)
        if accountapproval:
            return redirect('leader-dashboard')
        else:
            return render(request, 'recordsManagement/leader_await_approval.html')
    else:
        return render(request, 'recordsManagement/unknown-user.html')


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
    total_members = count_church_members + count_leaders

    admin_username = request.user
    context = {
        'leaders':leaders,
        'members':members,
        'count_leaders':count_leaders,
        'count_church_members':count_church_members,
        'pending_leaders_count':pending_leaders_count,
        'pending_members_count':pending_members_count,
        'total_members':total_members,
        'admin_username': admin_username,
    }
    return render(request, 'recordsManagement/admin_dashboard.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_members_view(request):
    return render(request, 'recordsManagement/admin-member.html')


# List/Table of all members(approved)
@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_list_members_view(request):
    members = models.ChurchMember.objects.all().filter(status=True)
    context = {"members": members}
    return render(request, 'recordsManagement/admin-list-members.html', context)


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
    return render(request, 'recordsManagement/admin-add-member.html', context)
    


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_delete_member_view(request, pk):
    member = models.ChurchMember.objects.get(id=pk)
    user = models.User.objects.get(id=member.user_id)
    messages.warning(request, "This action is irreversible!")
    print("******** Delete button clicked ********")
    member.delete()
    user.delete()
    print("********* Member deleted *****")
    messages.success(request, f"Success: {request.user} is Deleted!")
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

    return render(request, 'recordsManagement/admin-update-member.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_pending_approvals_member_view(request):
    members_pending = models.ChurchMember.objects.all().filter(status=False)
    context = {'members_pending': members_pending}
    return render(request, 'recordsManagement/pending_approvals_member.html', context)


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
    return render(request, 'recordsManagement/admin-leader.html')


# List/Table of all members(approved)
@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_list_leaders_view(request):
    leaders = models.ChurchLeader.objects.all().filter(status=True)
    context = {"leaders": leaders}
    return render(request, 'recordsManagement/admin-list-leaders.html', context)


# Admin actions on Church Leader views
@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_add_leader_view(request):
    userForm = forms.LeaderUserForm()
    leaderForm = forms.LeaderForm()
    context = {
        "userForm": userForm,
        "leaderForm": leaderForm
    }
    if request.method == "POST":
        userForm = forms.ChurchMemberUserForm(request.POST)
        leaderForm = forms.ChurchMemberForm(request.POST, request.FILES)
        if userForm.is_valid() and leaderForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            leader = leaderForm.save(commit=False)
            leader.user = user
            leader.status = True
            leader.save()

            leader_group = Group.objects.get_or_create(name="LEADERS")
            leader_group[0].user_set.add(user)
        messages.success(request, "Success: New Church Leader Added!")
        return redirect('admin-list-leaders')
    return render(request, 'recordsManagement/admin-add-leader.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_update_leader_view(request, pk):
    leader = models.ChurchLeader.objects.get(id=pk)
    user = models.User.objects.get(id=leader.user_id)

    leaderForm = forms.LeaderForm(request.FILES, instance=leader)
    userForm = forms.LeaderUserForm(instance=user)
    context = {
        'leaderForm': leaderForm,
        'userForm': userForm
    }
    if request.method == 'POST':
        leaderForm = forms.LeaderForm(request.POST, request.FILES, instance=leader)
        userForm = forms.LeaderUserForm(request.POST, instance=user)
        if userForm.is_valid() and leaderForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            leader = leaderForm.save(commit=False)
            leader.status = True
            leader.save()
        messages.success(request, "Success: Church Leader Updated!")
        return redirect('admin-list-leaders')

    return render(request, 'recordsManagement/admin-update-leader.html', context)




@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_pending_approvals_leader_view(request):
    leaders_pending = models.ChurchLeader.objects.all().filter(status=False)
    context = {'leaders_pending': leaders_pending}
    return render(request, 'recordsManagement/pending_approvals_leader.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def admin_approve_leader_view(request, pk):
    leaders = models.ChurchLeader.objects.get(id=pk)
    leaders.status = True
    leaders.save()
    messages.success(request, f"Leader Successfully Approved")
    return redirect('pending-leader')


@login_required(login_url='adminlogin')
@user_passes_test(is_churchadmin)
def reject_leader_view(request, pk):
    leader = models.ChurchLeader.objects.get(id=pk)
    user = models.User.objects.get(id=leader.user_id)
    leader.delete()
    user.delete()
    messages.success(request, f"{leader.username} was Rejected!")
    return redirect('pending-leader')




#<-----------------Views For Church Leader Only----------->
@login_required(login_url='execlogin')
@user_passes_test(is_churchleader)
def leader_dashboard_view(request):
    #to create three cards 
    # count_church_members = models.ChurchMember.objects.all().count()
    # count_leaders = models.ChurchLeader.objects.all().filter().count()
    # total_members = count_church_members + count_leaders
    # context = {
    #     'count_church_members':count_church_members,
    #     'count_leaders':count_leaders,
    #     'total_members':total_members,
    #     'leader':models.ChurchLeader.objects.get(user_id=request.user.id)
    #     #for profile picture of church leader in the sidebar
    # }
    leaders = models.ChurchLeader.objects.all().order_by('-id')
    count_leaders = models.ChurchLeader.objects.all().filter(status= True).count()
    pending_leaders_count = models.ChurchLeader.objects.all().filter(status=False).count()
    members = models.ChurchMember.objects.all().order_by('-id')
    count_church_members = models.ChurchMember.objects.all().filter(status=True).count()
    pending_members_count = models.ChurchMember.objects.all().filter(status=False).count()
    total_members = count_church_members + count_leaders

    admin_username = request.user
    context = {
        'leaders':leaders,
        'members':members,
        'count_leaders':count_leaders,
        'count_church_members':count_church_members,
        'pending_leaders_count':pending_leaders_count,
        'pending_members_count':pending_members_count,
        'total_members':total_members,
        'admin_username': admin_username,
    }
    return render(request, 'recordsManagement/exec_dashboard.html', context)


#<----------Views to Search for Church Members--------->
class SearchMembersView(ListView):
    model = models.ChurchMember
    context_object_name = "member_list"
    template_name = "RecordsManagement/searchresults_member.html"
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return models.ChurchMember.objects.filter(
            Q(user__icontains=query) | Q(member_role__icontains=query)
        )

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
