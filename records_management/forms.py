from django import forms
from django.contrib.auth.models import User
from . import models

#for admin signup
class AdminSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'username',
            'last_name',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

#for church leaders to create an account
#combine with ChurchLeader model in views to create a user form
class ExecutiveUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'username',
            'last_name',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }


class ExecutiveForm(forms.ModelForm):
    class Meta:
        model = models.ChurchLeader
        fields = '__all__'


#forms for church members to create an account
class ChurchMemberUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password'
        ]
        
class ChurchMemberForm(forms.ModelForm):
    class Meta:
        model = models.ChurchMember
        fields = '__all__'