from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom fields', {'fields': ('age', 'verification_code')}),
    )
    list_display = ['username', 'email', 'age', 'verification_code', 'is_staff']
    search_fields = ['username', 'email', 'verification_code']

admin.site.register(CustomUser, CustomUserAdmin)
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

