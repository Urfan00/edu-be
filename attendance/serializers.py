from rest_framework import serializers
from group.models import Group, UserGroup
from .models import Attendance
from django.utils.translation import gettext_lazy as _



class AttendanceCreateSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True, help_text=_("The name of the group."))
    student_passport_id = serializers.CharField(write_only=True, help_text=_("The passport ID of the student."))

    class Meta:
        model = Attendance
        fields = ['id', 'status', 'date', 'group_name', 'student_passport_id']
        read_only_fields = ['id']

    def validate(self, attrs):
        """
        Custom validation for attendance creation without using try-except.
        """
        group_name = attrs.get('group_name')
        student_passport_id = attrs.get('student_passport_id')
        date = attrs.get('date')

        # Check if the group exists
        group = Group.objects.filter(group_name=group_name).first()
        if not group:
            raise serializers.ValidationError({"group_name": _("Group with this name does not exist.")})

        # Check if the group is active
        if group.status != Group.Status.ACTIVE:
            raise serializers.ValidationError({"group_name": _("The specified group is not active.")})

        # Check if the student is part of the group
        user_group = UserGroup.objects.filter(group=group, student_passport_id=student_passport_id).first()
        if not user_group:
            raise serializers.ValidationError({"student_passport_id": _("Student is not part of the specified group.")})

        # Check if the user group is active
        if user_group.status != UserGroup.Status.ACTIVE:
            raise serializers.ValidationError({"student_passport_id": _("The student is not in an active group.")})

        # Check for duplicate attendance on the same date
        if Attendance.objects.filter(user_group=user_group, date=date).exists():
            raise serializers.ValidationError({"date": _("Attendance for this student on this date already exists.")})

        # Add resolved user group to validated data for later use
        attrs['user_group'] = user_group
        return attrs

    def create(self, validated_data):
        """
        Create a single attendance record.
        """
        validated_data.pop('group_name')
        validated_data.pop('student_passport_id')
        return Attendance.objects.create(**validated_data)


class AttendanceListSerializer(serializers.ModelSerializer):
    student_full_name = serializers.CharField(source='user_group.student_full_name')
    student_passport_id = serializers.CharField(source='user_group.student_passport_id')
    group_name = serializers.CharField(source='user_group.group.group_name')

    class Meta:
        model = Attendance
        fields = ['id', 'student_full_name', 'student_passport_id', 'group_name', 'status', 'date']
