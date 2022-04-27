from django.contrib import admin

from recordsManagement.models import ChurchMember, ChurchLeader

# Register your models here.
admin.site.register(ChurchMember)
admin.site.register(ChurchLeader)