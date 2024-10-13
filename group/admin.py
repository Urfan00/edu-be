from django.contrib import admin
from .models import Group, UserGroup
from import_export.admin import ImportExportModelAdmin


@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = ['id', 'group_name', 'teacher', 'operator', 'is_active', 'start_date', 'end_date']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['group_name', 'teacher__email', 'operator__email']
    ordering = ['group_name']
    readonly_fields = ['id']


@admin.register(UserGroup)
class UserGroupAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'group', 'average']
    list_filter = ['group', 'student']
    search_fields = ['student__email', 'group__group_name']
    ordering = ['group', 'student']
    readonly_fields = ['id']
