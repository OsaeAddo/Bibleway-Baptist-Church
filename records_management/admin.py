from django.contrib import admin
from .models import ChurchMember, ChurchLeader

# Register your models here.
admin.site.register(ChurchMember)
admin.site.register(ChurchLeader)