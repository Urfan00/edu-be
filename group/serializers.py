# serializers.py
from rest_framework import serializers
from .models import Group, UserGroup
from identity.models import User


class GroupSerializer(serializers.ModelSerializer):
    teacher = serializers.SlugRelatedField(
        slug_field="email", queryset=User.objects.filter(user_type="teacher")
    )
    operator = serializers.SlugRelatedField(
        slug_field="email", queryset=User.objects.filter(user_type="operator")
    )

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'teacher', 'operator',
                  'is_active', 'start_date', 'end_date']


class UserGroupSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(
        slug_field="email", queryset=User.objects.filter(user_type="student")
    )
    group = serializers.SlugRelatedField(
        slug_field="group_name", queryset=Group.objects.all())

    class Meta:
        model = UserGroup
        fields = ['id', 'student', 'group', 'average']
