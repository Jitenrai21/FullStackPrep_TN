from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active', 'mfa_enabled']
    list_filter = ['is_staff', 'is_active', 'mfa_enabled']
    fieldsets = UserAdmin.fieldsets + (
        ('MFA Settings', {'fields': ('mfa_secret', 'mfa_enabled')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('MFA Settings', {'fields': ('mfa_secret', 'mfa_enabled')}),
    )
    search_fields = ['username', 'email']
    ordering = ['email']

admin.site.register(CustomUser, CustomUserAdmin)
