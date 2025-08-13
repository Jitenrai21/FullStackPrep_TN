from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import UserData

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


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'extracted_text') 




# shop/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)


