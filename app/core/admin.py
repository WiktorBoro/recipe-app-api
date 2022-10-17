from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']


admin.site.register(User, UserAdmin)
