from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import (
    Purpose, SourceOfInformation, University, Filial, Region, Program, Register
)
from .serializers import (
    PurposeSerializer, RegisterUpdateSerializer, SourceOfInformationSerializer, UniversitySerializer,
    FilialSerializer, RegionSerializer, ProgramSerializer, RegisterSerializer
)


class PurposeViewSet(viewsets.ModelViewSet):
    queryset = Purpose.objects.all()
    serializer_class = PurposeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SourceOfInformationViewSet(viewsets.ModelViewSet):
    queryset = SourceOfInformation.objects.all()
    serializer_class = SourceOfInformationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FilialViewSet(viewsets.ModelViewSet):
    queryset = Filial.objects.all()
    serializer_class = FilialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()

    def get_permissions(self):
        if self.action == 'create':  # Allow unauthenticated access for POST requests
            return []  # No permissions required
        return [IsAuthenticated()]  # Require authentication for other actions

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return RegisterUpdateSerializer  # Use the limited serializer for updates
        return RegisterSerializer  # Use the default serializer for other actions
