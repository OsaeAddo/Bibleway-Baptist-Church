from django.shortcuts import render

# Create your views here.
def home_testapp(request):
    return render(request, 'testapp/test_home.html')