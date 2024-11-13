from django.contrib import admin
from .models import Group, UserGroup
from import_export.admin import ImportExportModelAdmin


@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = ['id', 'group_name', 'teacher_passport_id', 'teacher_full_name', 'mentor_passport_id', 'mentor_full_name', 'status', 'start_date', 'end_date', 'created_at', 'updated_at']
    list_filter = ['status', 'start_date', 'end_date', 'created_at', 'updated_at']
    search_fields = ['group_name', 'teacher_passport_id', 'teacher_full_name', 'mentor_passport_id', 'mentor_full_name']
    ordering = ['group_name']
    readonly_fields = ['id']


@admin.register(UserGroup)
class UserGroupAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student_passport_id', 'student_full_name', 'group', 'average', 'status', 'created_at', 'updated_at']
    list_filter = ['group', 'student_passport_id', 'student_full_name', 'status', 'created_at', 'updated_at']
    search_fields = ['student_passport_id', 'student_full_name', 'group__group_name']
    ordering = ['group', 'student_full_name']
    readonly_fields = ['id']
