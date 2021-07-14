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
    return render(request, 'RecordsManagement/access-level-page.html')