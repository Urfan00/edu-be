# urls.py
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, UserGroupViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'user-groups', UserGroupViewSet, basename='usergroup')

app_name = "group"

urlpatterns = [
    path('', include(router.urls)),
]
