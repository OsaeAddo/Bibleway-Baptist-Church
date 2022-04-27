from django import forms
from django.contrib.auth.models import User
from . import models

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
                'class': "placeholder-gray-500",
            }),
            'username': forms.TextInput(attrs={
                'placeholder':"Username",
                'class': "placeholder-gray-500",
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder':"Last name",
                'class': "placeholder-gray-500",
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder':"Password",
                'class': "placeholder-gray-500",
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
                'class': "placeholder-gray-500",
                'type': "tel",
            }),
            'emergency_contact': forms.TextInput(attrs={
                'placeholder': "Enter emergency contact",
                'class': "placeholder-gray-500",
                'label': "Emergency Contact",
                'type': "tel",
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': "w-4/5 placeholder-gray-500",
                'placeholder': "Date of Birth",
            }),
            'date_of_baptism': forms.DateInput(attrs={
                'class': "w-4/5 placeholder-gray-500", 
                'placeholder': "Date of Baptism",
            }),
            'name_of_father': forms.TextInput(attrs={
                'placeholder': "Enter father's name",
                'class': "placeholder-gray-500",
            }),
            'name_of_mother': forms.TextInput(attrs={
                'placeholder': "Enter mother's name",
                'class': "placeholder-gray-500",
            }),
            'hometown': forms.TextInput(attrs={
                'placeholder': "Hometown",
                'class': "placeholder-gray-500",
            }),
            'region': forms.TextInput(attrs={
                'placeholder': "Region",
                'class': "placeholder-gray-500",
            }),
            'residential_address': forms.TextInput(attrs={
                'placeholder': "Enter residential address",
                'class': "placeholder-gray-500",
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
            'username': forms.TextInput(attrs={
                'label': "User Name*"
            }),
            'last_name': forms.TextInput(attrs={'placeholder':"Last name"}),
            'password': forms.PasswordInput(attrs={'placeholder':"Password"}),
        }

        
class ChurchMemberForm(forms.ModelForm):
    class Meta:
        model = models.ChurchMember
        fields = '__all__'
        widgets = {
            'mobile': forms.TextInput(attrs={
                'placeholder': "Enter phone number",
                'class': "placeholder-gray-500",
                'type': "tel",
            }),
            'emergency_contact': forms.TextInput(attrs={
                'placeholder': "Enter emergency contact",
                'class': "placeholder-gray-500",
                'label': "Emergency Contact",
                'type': "tel",
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': "w-4/5 placeholder-gray-500",
                'placeholder': "Date of Birth",
            }),
            'date_of_baptism': forms.DateInput(attrs={
                'class': "w-4/5 placeholder-gray-500", 
                'placeholder': "Date of Baptism",
            }),
            'name_of_father': forms.TextInput(attrs={
                'placeholder': "Enter father's name",
                'class': "placeholder-gray-500",
            }),
            'name_of_mother': forms.TextInput(attrs={
                'placeholder': "Enter mother's name",
                'class': "placeholder-gray-500",
            }),
            'hometown': forms.TextInput(attrs={
                'placeholder': "Hometown",
                'class': "placeholder-gray-500",
            }),
            'region': forms.TextInput(attrs={
                'placeholder': "Region",
                'class': "placeholder-gray-500",
            }),
            'residential_address': forms.TextInput(attrs={
                'placeholder': "Enter residential address",
                'class': "placeholder-gray-500",
            }),
        }