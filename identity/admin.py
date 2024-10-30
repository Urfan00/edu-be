from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from identity.models import AccessToken, User, Role
from django.utils import timezone
from django.utils.translation import ngettext_lazy, gettext_lazy as _
from import_export.admin import ImportExportModelAdmin


# Register Permission model to admin
@admin.register(Permission)
class PermissionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'codename', 'content_type']
    search_fields = ['name', 'codename']
    list_filter = ['content_type']
    ordering = ['id']


# Customizing the RoleAdmin to manage permissions within roles
@admin.register(Role)
class RoleAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'status', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['permissions']  # Allow multi-select for permissions


# Customizing UserAdmin to display additional fields
@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'father_name', 'passport_id', 'profile_image', 'gender', 'user_type')}),
        (_('Contact info'), {'fields': ('phone_number_1', 'phone_number_2', 'address')}),
        (_('Social media'), {
            'fields': ('instagram', 'facebook', 'twitter', 'github', 'youtube', 'linkedin'),
            'classes': ['collapse']
        }),
        (_('Roles and Permissions'), {'fields': ('roles', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Status'), {'fields': ('first_time_login', 'is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password', 'first_name', 'last_name', 'father_name', 'gender', 'phone_number_1', 'phone_number_2', 'passport_id', 'user_type'),
        }),
        (_('Optional info'), {
            'fields': ('profile_image', 'bio', 'instagram', 'facebook', 'twitter', 'github', 'youtube', 'linkedin', 'address', 'roles'),
        }),
        (_('Status'), {
            'fields': ('first_time_login', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Fields to be displayed in the list view
    list_display = ['id', 'email', 'first_name', 'last_name', 'passport_id', 'user_type']
    
    # Fields to filter by in the list view
    list_filter = ['is_superuser', 'is_staff', 'is_active', 'user_type', 'first_time_login']

    # Add search functionality for these fields
    search_fields = ['email', 'first_name', 'last_name', 'passport_id', 'phone_number_1', 'phone_number_2']

    # Specify which fields can use filter_horizontal (multi-select in the admin)
    filter_horizontal = ['roles']

    ordering = ['email']

    # Field used to identify users for login
    ordering = ['email']

    readonly_fields = ['id', 'last_login', 'date_joined']


@admin.register(AccessToken)
class AccessTokenAdmin(ImportExportModelAdmin):
    actions = ("action_delete_expired_tokens",)
    list_display = (
        "jti",
        "user",
        "created_at",
        "expires_at",
        "is_active"
    )
    list_display_links = list_display
    list_filter = ("is_active",)
    search_fields = ("jti",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description=_("Delete selected expired tokens"))
    def action_delete_expired_tokens(self, request, queryset):
        expired_tokens = queryset.filter(expires_at__lt=timezone.now())
        count = expired_tokens.count()

        expired_tokens.delete()

        message = ngettext_lazy(
            "Successfully deleted {count} expired token.",
            "Successfully deleted {count} expired tokens.",
            count
        ).format(count=count)

        self.message_user(request, message, level=messages.SUCCESS)

