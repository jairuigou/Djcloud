from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Filepath
from django.contrib.auth.models import User
from django.contrib.auth import admin as auth_admin
# Register your models here.

class UserAdmin(auth_admin.UserAdmin):
    list_display = ['username','email','last_login','is_staff']
admin.site.unregister(User)
admin.site.register(User,UserAdmin)