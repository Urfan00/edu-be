from rest_framework import serializers
from group.models import Group, UserGroup
from identity.models import User
from identity.utils import send_registration_email
from .models import (
    Purpose, SourceOfInformation, University, Filial, Region, Program, Register
)


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = ['id', 'name']


class SourceOfInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceOfInformation
        fields = ['id', 'name']


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name']


class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'name']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'first_name' , 'last_name' , 'father_name' , 'email' , 'passport_id' , 'phone_number_1' , 'phone_number_2' , 'gender' , 'lesson_type', 'purpose' , 'source_of_information' , 'university' , 'filial' , 'region' , 'program']

    def validate(self, attrs):
        # Dictionary to hold field names and corresponding model references
        validation_mapping = {
            'purpose': Purpose,
            'source_of_information': SourceOfInformation,
            'university': University,
            'filial': Filial,
            'region': Region,
            'program': Program,
        }

        # Loop through each field and verify existence in the corresponding model
        for field, model in validation_mapping.items():
            value = attrs.get(field)
            if value and not model.objects.filter(name=value).exists():
                raise serializers.ValidationError({field: f"The specified {field} '{value}' does not exist."})

        # Return the validated data if all checks pass
        return attrs


class RegisterUpdateSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False, write_only=True)

    class Meta:
        model = Register
        fields = ['status', 'group']

    def validate(self, attrs):
        status = attrs.get('status')
        group = attrs.get('group')

        # Validate that a group is provided if status is set to "active"
        if status == Register.Status.ACTIVE and not group:
            raise serializers.ValidationError({"group": "Group is required when status is set to active."})

        return attrs

    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)
        group = validated_data.get('group')

        # Update the status in the Register instance
        instance.status = status
        instance.save()


        if status == Register.Status.ACTIVE and group:
            # Check if a User with this passport_id already exists
            if User.objects.filter(passport_id=instance.passport_id).exists():
                raise serializers.ValidationError({"user": "User with this passport ID already exists."})

            # User creation section if the User does not already exist
            user_data = {
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'father_name': instance.father_name,
                'email': instance.email,
                'passport_id': instance.passport_id,
                'phone_number_1': instance.phone_number_1,  # Assuming phone_number_1 maps to User's phone_number
                'phone_number_2': instance.phone_number_2,  # Assuming phone_number_1 maps to User's phone_number
                'gender': instance.gender,
                'user_type': User.UserTypeChoices.STUDENT  # Default user_type as STUDENT
            }
            user = User(**user_data)
            user.set_password(instance.passport_id)  # Set an initial password as passport_id
            user.save()

            send_registration_email(user)

            # Create UserGroup if the status is active and group is provided
            UserGroup.objects.create(student=user, group=group, status=UserGroup.Status.ACTIVE, average=0.0)

        return instance