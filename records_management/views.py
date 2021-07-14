from django.shortcuts import render
from django.db.models import Q #for more sophisticated/realistic queries
from . import models, forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    return render(request, 'records_management/access-level-page.html')

def accesslevel_view(request):
    return render(request, 'records_management/access-level-page.html')

#Shows the signup/login for Church Admin
def churchAdminClick_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request, 'records_management/churchadmin-click.html')

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
            return HttpResponseRedirect('/church-admin-login/')
    else:
        adminForm = forms.AdminSignupForm()
    return render(request, 'RecordsManagement/adminsignup.html', {'adminForm': adminForm})