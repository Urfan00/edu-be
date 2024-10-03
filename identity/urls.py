from django.urls import path, include
from identity.views import ChangePasswordView, CustomTokenObtainPairView, CustomTokenRefreshView, PasswordResetRequestView, PermissionViewSet, ResetPasswordView, UserBulkUploadView, UserViewSet, RoleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')

app_name = "identity"

urlpatterns = [
    path('', include(router.urls)),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('request-reset-password/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='password_reset'),
    path('bulk-create/', UserBulkUploadView.as_view(), name='user-bulk-upload'),
]
