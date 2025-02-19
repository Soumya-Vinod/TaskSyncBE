from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Team

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'team', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'profile_picture', 'bio', 'phone_number')}),
        ('Team & Role', {'fields': ('role', 'team')}),
        ('Notifications', {'fields': ('email_notifications', 'push_notifications')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Team)
