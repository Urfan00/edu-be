# serializers.py
from rest_framework import serializers
from .models import Group, UserGroup
from identity.models import User
from django.utils.translation import gettext_lazy as _


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
                  'status', 'start_date', 'end_date']

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                "start_date": _("Start date cannot be later than end date.")
            })
        return data


class UserGroupSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(
        slug_field="email", queryset=User.objects.filter(user_type="student")
    )
    group = serializers.SlugRelatedField(
        slug_field="group_name", queryset=Group.objects.all())

    class Meta:
        model = UserGroup
        fields = ['id', 'student', 'group', 'average']
