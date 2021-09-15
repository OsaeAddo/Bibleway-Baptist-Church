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
            'first_name': forms.TextInput(attrs={
                'placeholder':"First name",
                'size': 20,
                'class': "placeholder-gray-900",
            }),
            'username': forms.TextInput(attrs={
                'placeholder':"Username",
                'class': "placeholder-gray-900",
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder':"Last name",
                'class': "placeholder-gray-900",
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder':"Password",
                'class': "placeholder-gray-900",
            }),
        }


class LeaderForm(forms.ModelForm):
    class Meta:
        model = models.ChurchLeader
        fields = '__all__'
        widgets = {
            # 'leadershiptype': forms.Input(attrs={
            #     'placholder': "Select Role",
            #     'label': "leadership role",
            # }),
            'mobile': forms.TextInput(attrs={
                'placeholder': "Enter phone number",
                'class': "placeholder-gray-900",
            }),
            'emergency_contact': forms.TextInput(attrs={
                'placeholder': "Emergency contact",
                'class': "placeholder-gray-900",
                'label': "Emergency Contact",
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': "w-4/5 placeholder-gray-900",
                'placeholder': "Date of Birth",
            }),
            'date_of_baptism': forms.DateInput(attrs={
                'class': "w-4/5 placeholder-gray-900", 
                'placeholder': "Date of Baptism",
            }),
            'name_of_father': forms.TextInput(attrs={
                'placeholder': "Name of father",
                'class': "placeholder-gray-900",
            }),
            'name_of_mother': forms.TextInput(attrs={
                'placeholder': "Name of mother",
                'class': "placeholder-gray-900",
            }),
            'hometown': forms.TextInput(attrs={
                'placeholder': "Hometown",
                'class': "placeholder-gray-900",
            }),
            'region': forms.TextInput(attrs={
                'placeholder': "Region",
                'class': "placeholder-gray-900",
            }),
            'residential_address': forms.TextInput(attrs={
                'placeholder': "Residential address",
                'class': "placeholder-gray-900",
            }),
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