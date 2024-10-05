from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from drf_yasg.utils import swagger_auto_schema

import pandas as pd

from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from identity.models import User, Role
from identity.serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer,
    TokenRefreshResponseSerializer,
    UserBulkUploadSerializer,
    UserSerializer,
    UserCreateUpdateSerializer,
    RoleSerializer,
    TokenObtainPairResponseSerializer,
)
from identity.utils import send_registration_email


# Role ViewSet
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateUpdateSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """
        Custom logic during user creation.
        """
        user = serializer.save()
        send_registration_email(user)


class UserBulkUploadView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserBulkUploadSerializer
    parser_classes = (MultiPartParser, FormParser)  # To handle file uploads

    def post(self, request, *args, **kwargs):
        """
        POST method to handle bulk user uploads via CSV or Excel file.
        """
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the file is in CSV or Excel format
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                return Response({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Process the DataFrame with user data
            return self.handle_user_data(df)

        except Exception as e:
            return Response({"error": f"Error processing the file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def handle_user_data(self, df):
        errors = []
        users_to_create = []

        df = df.where(pd.notnull(df), None)

        for index, row in df.iterrows():
            user_data = {
                'email': row['email'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'father_name': row['father_name'],
                'gender': row['gender'],
                'phone_number': row['phone_number'],
                'passport_id': row['passport_id'],
                'user_type': row['user_type'],
                'bio': row.get('bio', None),
                'instagram': row.get('instagram', None),
                'facebook': row.get('facebook', None),
                'twitter': row.get('twitter', None),
                'github': row.get('github', None),
                'youtube': row.get('youtube', None),
                'linkedin': row.get('linkedin', None),
                'address': row.get('address', None)
            }

            # Handle roles if present
            roles = row.get('roles', '')
            if roles:
                role_names = [role.strip() for role in roles.split(',')]
                role_objects = Role.objects.filter(name__in=role_names)
                user_data['roles'] = role_objects

            # Try to create the user
            serializer = UserCreateUpdateSerializer(data=user_data)
            try:
                serializer.is_valid(raise_exception=True)
                users_to_create.append(user_data)
            except ValidationError as ve:
                errors.append(f"Row {index + 1}: {str(ve)}")
            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")

        # Return the response with errors (if any) and the list of created users
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        
        with transaction.atomic():  # Start a new transaction
            created_users = []
            for user_data in users_to_create:
                serializer = UserCreateUpdateSerializer(data=user_data)
                if serializer.is_valid():
                    user = serializer.save()  # Save user and check for errors
                    send_registration_email(user)
                    created_users.append(user.email)

        return Response({"message": "Users created successfully", "created_users": created_users}, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        tags=["JWT Authentication"],
        operation_description=(
            "Takes a set of user credentials and returns an access and refresh JSON web token pair "
            "along with user details to prove the authentication of those credentials."
        ),
        responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    @swagger_auto_schema(
        tags=["JWT Authentication"],
        operation_description=(
            "Takes a refresh type JSON web token and returns an access type JSON web "
            "token if the refresh token is valid."
        ),
        responses={status.HTTP_200_OK: TokenRefreshResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Invalid reset request.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct reset link
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # Send email
        subject = "Password Reset Request"
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return Response({"detail": _("Password reset link has been sent to your email.")})


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'message': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        # Reset password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": _("Password has been reset successfully.")})
