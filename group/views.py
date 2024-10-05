from rest_framework import viewsets
from .models import Group, UserGroup
from .serializers import GroupSerializer, UserGroupSerializer
from rest_framework.permissions import IsAuthenticated

class GroupViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing group instances.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class UserGroupViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user group instances.
    """
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = [IsAuthenticated]
