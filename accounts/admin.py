from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = list(UserAdmin.fieldsets) + [
        ('Additional Info', {'fields': ('role', 'phone')}),
    ]

    add_fieldsets = list(UserAdmin.add_fieldsets) + [
        ('Additional Info', {'fields': ('role', 'phone')}),
    ]

    list_display = ['username', 'email', 'role', 'phone', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']


admin.site.register(User, CustomUserAdmin)
