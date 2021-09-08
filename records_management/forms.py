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
            'first_name': forms.TextInput(attrs={'placeholder':"First name"}),
            'username': forms.TextInput(attrs={'placeholder':"Username"}),
            'last_name': forms.TextInput(attrs={'placeholder':"Last name"}),
            'password': forms.PasswordInput(attrs={'placeholder':"Password"}),
        }

#for church leaders to create an account
#combine with ChurchLeader model in views to create a user form
class LeaderUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'username',
            'last_name',
            'password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':"First name"}),
            'username': forms.TextInput(attrs={'placeholder':"Username"}),
            'last_name': forms.TextInput(attrs={'placeholder':"Last name"}),
            'password': forms.PasswordInput(attrs={'placeholder':"Password"}),
        }


class LeaderForm(forms.ModelForm):
    class Meta:
        model = models.ChurchLeader
        fields = '__all__'
        widgets = {
            'mobile': forms.TextInput(attrs={'placeholder': "Enter phone number"}),
            'emergency_contact': forms.TextInput(attrs={'placeholder': "Enter emergency contact"}),
            'name_of_father': forms.TextInput(attrs={'placeholder': "Name of father"}),
            'name_of_mother': forms.TextInput(attrs={'placeholder': "Name of mother"}),
            'hometown': forms.TextInput(attrs={'placeholder': "Hometown"}),
            'region': forms.TextInput(attrs={'placeholder': "Region"}),
            'residential_address': forms.TextInput(attrs={'placeholder': "Residential address"}),
        }


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
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':"First name"}),
            'username': forms.TextInput(attrs={'placeholder':"Username"}),
            'last_name': forms.TextInput(attrs={'placeholder':"Last name"}),
            'password': forms.PasswordInput(attrs={'placeholder':"Password"}),
        }

        
class ChurchMemberForm(forms.ModelForm):
    class Meta:
        model = models.ChurchMember
        fields = '__all__'