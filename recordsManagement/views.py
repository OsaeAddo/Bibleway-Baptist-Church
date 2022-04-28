from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from recordsManagement import models, forms

# Create your views here.
def home(request):
    return render(request, 'recordsManagement/home.html')

