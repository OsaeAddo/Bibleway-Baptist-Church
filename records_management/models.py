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