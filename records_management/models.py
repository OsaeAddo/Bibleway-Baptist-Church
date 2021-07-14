from django.db import models
from django.contrib.auth.models import User
from django.utils import time_zone
# Create your models here.
member_roles = [
    ('Singer', 'Singer'),
    ('Usher', 'Usher'),
    ('Instrumentalist', 'Instrumentalist'),
    ('Cleaner', 'Cleaner'),
    ('Choirester', 'Choirester'),
    ('Secretary', 'Secretary'),
    ('Treasurer', 'Treasurer'),
]

leadershiptypes = [
    ('Head Pastor', 'Head Pastor'),
    ('Junior Pastor', 'Junior Pastor'),
    ('Prophet', 'Prophet'),
    ('Evangelist', 'Evangelist'),
    ('Elder', 'Elder'),
    ('Minister', 'Minister'),
    ('Deacon', 'Deacon'),
    ('Deaconess', 'Deaconess'),
]
marital_statuses = [
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Widowed', 'Widowed'),
    ('Divorced', 'Divorced'),
    ('Other', 'Other'),
]

genders = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('Other', 'Other'),
]


class ChurchMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=genders, blank=True, null=True)
    member_role = models.CharField(max_length=60, choices=member_roles, default='', blank=True, null=True)
    date_of_birth = models.DateField(default=timezone.now)
    marital_status = models.CharField(max_length=30, choices=marital_statuses, default='Single')
    mobile = models.CharField(max_length=11, blank=True, null=True)
    emergency_contact = models.CharField(max_length=11, blank=True, null=True)
    name_of_father = models.CharField(max_length=60, blank=True, null=True)
    name_of_mother = models.CharField(max_length=60, blank=True, null=True)
    hometown = models.CharField(max_length=60, blank=True, null=True)
    region = models.CharField(max_length=60, blank=True, null=True)
    residential_address = models.CharField(max_length=60,)
    date_of_baptism = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)



    class Meta:
        verbose_name_plural = 'Church Members'
    def __str__(self):
        return self.user.first_name + self.user.last_name + '('+self.member_role+')'


class ChurchLeader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    leadershiptype = models.CharField(max_length=30, choices=leadershiptypes, default='')
    date_of_birth = models.DateField(default=timezone.now)
    marital_status = models.CharField(max_length=30, choices=marital_statuses, default='Single')
    mobile = models.CharField(max_length=11, blank=True, null=True)
    emergency_contact = models.CharField(max_length=11, blank=True, null=True)
    name_of_father = models.CharField(max_length=60)
    name_of_mother = models.CharField(max_length=60)
    hometown = models.CharField(max_length=60, blank=True, null=True)
    region = models.CharField(max_length=60, blank=True, null=True)
    residential_address = models.CharField(max_length=60,)
    date_of_baptism = models.DateField(default=timezone.now)
    profile_pic = models.ImageField(upload_to='profile_pic/LeadersProfilePic/', null=True, blank=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def get_id(self):
        return self.user.id

    class Meta:
        verbose_name_plural = 'Church Leaders'

    def __str__(self):
        return f"{self.user.first_name} ({self.leadershiptype})"


