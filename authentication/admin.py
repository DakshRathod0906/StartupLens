from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, UserLoginHistory

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    """
    Custom administration panel for the User model.
    """
    list_display = ('username', 'email', 'role', 'is_active', 'is_verified', 'date_joined')
    list_filter = ('role', 'is_active', 'is_verified')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture', 'bio')}),
        ('Permissions', {
            'fields': ('is_active', 'is_verified', 'role', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

@admin.register(UserLoginHistory)
class UserLoginHistoryAdmin(admin.ModelAdmin):
    """
    Administration panel for User Login History.
    """
    list_display = ('user', 'ip_address', 'login_at', 'successful_login')
    list_filter = ('successful_login', 'login_at')
    search_fields = ('user__username', 'user__email', 'ip_address')
    list_select_related = ('user',)
    ordering = ('-login_at',)
    readonly_fields = ('user', 'ip_address', 'user_agent', 'login_at', 'successful_login')

    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
