from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from identity.models import User, Role
from identity.serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    SetNewPasswordSerializer,
    TokenRefreshResponseSerializer,
    UserSerializer,
    UserCreateUpdateSerializer,
    RoleSerializer,
    PermissionSerializer,
    TokenObtainPairResponseSerializer,
)


# Permission ViewSet
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


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
        serializer.save()


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Password changed successfully.")})


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Invalid reset request.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": _("Password has been reset successfully.")})
