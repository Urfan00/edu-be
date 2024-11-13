from rest_framework import serializers
from .models import Group, UserGroup
from identity.models import User
from django.utils.translation import gettext_lazy as _


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id', 'group_name', 'teacher_passport_id', 'teacher_full_name',
            'mentor_passport_id', 'mentor_full_name', 'status', 'start_date', 'end_date'
        ]

    def validate(self, data):
        # Validate and populate teacher's full name
        teacher_passport_id = data.get('teacher_passport_id')
        if teacher_passport_id:
            try:
                teacher = User.objects.get(passport_id=teacher_passport_id, user_type="teacher")
                data['teacher_full_name'] = teacher.get_full_name()
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "teacher_passport_id": _("Teacher with this passport ID does not exist.")
                })

        # Validate and populate mentor's full name
        mentor_passport_id = data.get('mentor_passport_id')
        if mentor_passport_id:
            try:
                mentor = User.objects.get(passport_id=mentor_passport_id, user_type="staff")
                data['mentor_full_name'] = mentor.get_full_name()
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "mentor_passport_id": _("Mentor with this passport ID does not exist.")
                })

        # Validate dates
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                "start_date": _("Start date cannot be later than end date.")
            })
        return data


class UserGroupSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field="group_name", queryset=Group.objects.all())

    class Meta:
        model = UserGroup
        fields = [
            'id', 'student_passport_id', 'student_full_name', 'group', 'average', 'status'
        ]

    def validate(self, data):
        # Validate and populate student's full name
        student_passport_id = data.get('student_passport_id')
        if student_passport_id:
            try:
                student = User.objects.get(passport_id=student_passport_id, user_type="student")
                data['student_full_name'] = student.get_full_name()
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "student_passport_id": _("Student with this passport ID does not exist.")
                })

        return data