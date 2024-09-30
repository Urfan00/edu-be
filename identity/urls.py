from django.urls import path, include
from identity.views import ChangePasswordView, CustomTokenObtainPairView, CustomTokenRefreshView, PermissionViewSet, ResetPasswordView, UserViewSet, RoleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')  # Add PermissionViewSet

app_name = "identity"

urlpatterns = [
    path('', include(router.urls)),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
