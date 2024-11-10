from rest_framework import serializers
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from group.models import Group, UserGroup
from identity.models import (
    User,
    Role,
    AccessToken as AccessTokenModel
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.utils import datetime_from_epoch


# Serializer for Permission Model (Many-to-Many in Role)
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name']
        read_only_fields = ['id']


# Serializer for Role Model
class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        write_only=True,
    )
    permissions_detail = PermissionSerializer(
        source="permissions",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'status',
                  'permissions', 'permissions_detail']

    def validate_permissions(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("Permissions are required.")
        return value


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'status']


# Serializer for User Model
class UserSerializer(serializers.ModelSerializer):
    # dinamik permissionlar olanda role elave edilmelidi
    # roles = UserRoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'father_name', 'gender',
            'profile_image', 'bio', 'phone_number_1', 'phone_number_2', 'passport_id',
            'instagram', 'facebook', 'twitter', 'github', 'youtube',
            'linkedin', 'address', 'first_time_login', 'user_type'
        ]

        # dinamik permissionlar olanda role elave edilmelidi
        # fields = [
        #     'id', 'email', 'first_name', 'last_name', 'father_name', 'gender',
        #     'profile_image', 'bio', 'phone_number_1', 'phone_number_2', 'passport_id',
        #     'instagram', 'facebook', 'twitter', 'github', 'youtube',
        #     'linkedin', 'address', 'roles', 'first_time_login', 'user_type'
        # ]


class UserFilterSerializer(serializers.Serializer):
    user_type = serializers.CharField(required=True)

    def validate_user_type(self, value):
        allowed_types = {'teacher', 'student', 'parent', 'staff', 'director'}
        if value not in allowed_types:
            raise serializers.ValidationError(
                _("Invalid user_type. Allowed values are: teacher, student, parent, staff, director.")
            )
        return value


# Serializer for User Creation/Update (with roles and permissions)
class UserCreateUpdateSerializer(serializers.ModelSerializer):
    # roles = serializers.PrimaryKeyRelatedField(
    #     queryset=Role.objects.all(), many=True, required=False
    # )

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'father_name', 'gender',
            'profile_image', 'bio', 'phone_number_1', 'phone_number_2',
            'passport_id', 'instagram', 'facebook', 'twitter', 'github',
            'youtube', 'linkedin', 'address', 'first_time_login', 'user_type'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'father_name': {'required': True},
            'email': {'required': True},
            'passport_id': {'required': True},
            'phone_number_1': {'required': True},
            'phone_number_2': {'required': True},
            'user_type': {'required': True},
            'gender': {'required': True},
            'first_time_login': {'default': True, 'read_only': True},
            'instagram': {'allow_blank': True, 'required': False},
            'facebook': {'allow_blank': True, 'required': False},
            'twitter': {'allow_blank': True, 'required': False},
            'github': {'allow_blank': True, 'required': False},
            'youtube': {'allow_blank': True, 'required': False},
            'linkedin': {'allow_blank': True, 'required': False},
            'address': {'allow_blank': True, 'required': False},
            # 'roles': {'required': False}
        }

    def validate(self, data):
        user_type = data.get('user_type')

        if user_type not in ["teacher", "parent", "director", "staff"]:
            raise serializers.ValidationError(
                    {"user_type": _("Invalid user type. Must be 'teacher', 'parent', 'director', or 'staff'.")}
                )

        return data

    def create(self, validated_data):
        # roles_data = validated_data.pop('roles', [])
        password = validated_data.get('passport_id')

        user = User(**validated_data)
        user.set_password(password)
        user.first_time_login = True
        user.save()

        # if roles_data:
        #     user.roles.set(roles_data)

        return user

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', None)
        group = validated_data.pop('group', None)

        # Remove passport_id if present to prevent it from being updated
        # update yazilanda duzelis edilecek!
        # validated_data.pop('passport_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if roles_data is not None:
            instance.roles.set(roles_data)

        # Handle group assignment if user is a student
        if UserGroup.objects.filter(student=instance, group=group).exists():
            raise serializers.ValidationError("User is already assigned to this group.")

        if validated_data.get('user_type') == 'student' and group:
            UserGroup.objects.create(student=instance, group=group, average=0.0)

        return instance


class UserBulkUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class UserJwtSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "father_name",
            "first_time_login",
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": _("Invalid credentials, please check your email and password.")
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user"] = {
            field: getattr(user, field)
            for field in UserJwtSerializer.Meta.fields
            if hasattr(user, field) and field != "id"
        }
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Blacklist old refresh tokens
        self._blacklist_old_refresh_tokens(user, data.get("refresh"))
        # Deactivate old access tokens (mark them as inactive)
        self._deactivate_old_access_tokens(user)
        # Save the new access token in the database
        self._save_new_access_token(user, data.get("access"))

        # Add the user information to the response data
        data["user"] = UserJwtSerializer(user).data
        return data

    def _blacklist_old_refresh_tokens(self, user, current_refresh_token):
        if current_refresh_token:
            try:
                current_refresh_jti = RefreshToken(
                    current_refresh_token).get("jti")
                # Find all outstanding tokens for the user, excluding the current one
                previous_tokens = OutstandingToken.objects.filter(
                    user=user).exclude(jti=current_refresh_jti)
                # Bulk create blacklisted tokens for all previous tokens
                BlacklistedToken.objects.bulk_create(
                    [BlacklistedToken(token=token)
                     for token in previous_tokens],
                    ignore_conflicts=True
                )
            except Exception as e:
                raise ValueError(f"Error blacklisting old refresh tokens: {e}")

    def _deactivate_old_access_tokens(self, user):
        AccessTokenModel.objects.filter(
            user=user, is_active=True).update(is_active=False)

    def _save_new_access_token(self, user, current_access_token):
        if current_access_token:
            try:
                # Parse the current access token
                access_token = AccessToken(current_access_token)
                # Create a new record in the AccessToken model
                AccessTokenModel.objects.create(
                    user=user,
                    jti=access_token["jti"],
                    token=current_access_token,
                    created_at=datetime_from_epoch(access_token["iat"]),
                    expires_at=datetime_from_epoch(access_token["exp"]),
                )
            except Exception as e:
                raise ValueError(f"Error saving access token: {e}")


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Save the new access token in the database
        self._save_new_access_token(data.get("access"))
        return data

    def _save_new_access_token(self, new_access_token):
        if new_access_token:
            try:
                # Parse the new access token
                access_token = AccessToken(new_access_token)
                user = User.objects.get(id=access_token["user_id"])
                # Create a new record in the AccessToken model
                AccessTokenModel.objects.create(
                    user=user,
                    jti=access_token["jti"],
                    token=new_access_token,
                    created_at=datetime_from_epoch(access_token["iat"]),
                    expires_at=datetime_from_epoch(access_token["exp"]),
                )
            except Exception as e:
                raise ValueError(f"Error saving new access token: {e}")


class TokenObtainPairResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserJwtSerializer()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"})
    new_password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"})

    def validate_old_password(self, value):
        if self.instance and not self.instance.check_password(value):
            raise serializers.ValidationError(_("Old password is incorrect."))
        return value

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])

        if user.first_time_login:
            user.first_time_login = False

        user.save()


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        style={"input_type": "password"}
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        max_length=128,
        required=True,
        style={"input_type": "password"}
    )

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": _("Passwords do not match.")}
            )
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "There is no user registered with this email address.")
        return value
