from django.contrib import admin
from attendance.models import Attendance
from import_export.admin import ImportExportModelAdmin



@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user_group', 'status', 'date', 'get_student_full_name', 'created_at', 'updated_at')
    list_filter = ('status', 'date', 'user_group__group', 'created_at', 'updated_at')
    search_fields = ('user_group__student_full_name', 'user_group__student_passport_id', 'user_group__group__group_name')
    list_editable = ('status', )
    list_per_page = 10
    ordering = ('-date',)

    def get_student_full_name(self, obj):
        """Returns the student's full name from the user_group."""
        return obj.user_group.student_full_name
    get_student_full_name.short_description = "Student Full Name"