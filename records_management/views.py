from django.shortcuts import render
from django.db.models import Q #for more sophisticated/realistic queries
from . import models, forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect

# Create your views here.
