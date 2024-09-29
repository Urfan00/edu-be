from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from identity.models import User, Role
from django.utils.translation import gettext_lazy as _

# Register Permission model to admin
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'codename', 'content_type']
    search_fields = ['name', 'codename']
    list_filter = ['content_type']
    ordering = ['id']


# Customizing the RoleAdmin to manage permissions within roles
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['permissions']  # Allow multi-select for permissions


# Customizing UserAdmin to display additional fields
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'father_name', 'gender')}),
        (_('Contact info'), {'fields': ('phone_number', 'address')}),
        (_('Social media'), {
            'fields': ('instagram', 'facebook', 'twitter', 'github', 'youtube', 'linkedin'),
            'classes': ['collapse']
        }),
        (_('Roles and Permissions'), {'fields': ('roles', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Status'), {'fields': ('first_time_login', 'is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password', 'first_name', 'last_name', 'father_name', 'gender', 'phone_number', 'passport_id'),
        }),
        (_('Optional info'), {
            'fields': ('profile_image', 'bio', 'instagram', 'facebook', 'twitter', 'github', 'youtube', 'linkedin', 'address', 'roles'),
        }),
        (_('Status'), {
            'fields': ('first_time_login', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Fields to be displayed in the list view
    list_display = ['id', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'first_time_login']
    
    # Fields to filter by in the list view
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'user_type', 'first_time_login']

    # Add search functionality for these fields
    search_fields = ['email', 'first_name', 'last_name', 'passport_id', 'phone_number']

    # Specify which fields can use filter_horizontal (multi-select in the admin)
    filter_horizontal = ['roles']

    ordering = ['email']

    # Field used to identify users for login
    ordering = ['email']
    filter_horizontal = ['groups', 'user_permissions']

    readonly_fields = ['id', 'last_login', 'date_joined']
