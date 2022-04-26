from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from PIL import Image
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
    ('Select role', 'Select role'),
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
    profile_pic = models.ImageField(upload_to='profile_pic/members-profile-pic/', null=True, blank=True, default="admin-icon.png")
    gender = models.CharField(max_length=10, choices=genders, default='Gender', blank=True, null=True)
    member_role = models.CharField(max_length=60, choices=member_roles, default='Role', blank=True, null=True)
    date_of_birth = models.DateField(default=timezone.now)
    marital_status = models.CharField(max_length=30, choices=marital_statuses, default='Marital status')
    mobile = models.CharField(max_length=11, blank=True, null=True)
    emergency_contact = models.CharField(max_length=11, blank=True, null=True)
    name_of_father = models.CharField(max_length=60, blank=True, null=True)
    name_of_mother = models.CharField(max_length=60, blank=True, null=True)
    hometown = models.CharField(max_length=60, blank=True, null=True)
    region = models.CharField(max_length=60, blank=True, null=True)
    residential_address = models.CharField(max_length=60,)
    date_of_baptism = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_id(self):
        return self.user.id

    class Meta:
        verbose_name_plural = 'Church Members'

    # resize/reduce images saved to the files system
    def save(self):
        super().save()
        pic = Image.open(self.profile_pic.path)
        if pic.height > 300 or pic.width > 300:
            output_size = (300, 300)
            pic.thumbnail(output_size) #resize image
            pic.save(self.profile_pic.path)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.member_role})"


class ChurchLeader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/leaders-profile-pic/', null=True, blank=True, default="admin-icon.png")
    gender = models.CharField(max_length=10, choices=genders, default='Gender', null=True, blank=True,)
    leadershiptype = models.CharField(max_length=30, choices=leadershiptypes, default='Select Role')
    date_of_birth = models.DateField(default=timezone.now)
    marital_status = models.CharField(max_length=30, choices=marital_statuses, default='Single')
    mobile = models.CharField(max_length=11, null=True, blank=True,)
    emergency_contact = models.CharField(max_length=11, null=True, blank=True,)
    name_of_father = models.CharField(max_length=60, null=True, blank=True)
    name_of_mother = models.CharField(max_length=60, null=True, blank=True)
    hometown = models.CharField(max_length=60, null=True, blank=True,)
    region = models.CharField(max_length=60, null=True, blank=True,)
    residential_address = models.CharField(max_length=60)
    date_of_baptism = models.DateField(default=timezone.now, null=True, blank=True)
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
        return f"{self.user.first_name} {self.user.last_name} ({self.leadershiptype})"


