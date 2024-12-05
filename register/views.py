from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import (
    Purpose, SourceOfInformation, University, Filial, Region, Program, Register
)
from .serializers import (
    PurposeSerializer, RegisterInformationSerializer, RegisterUpdateSerializer, SourceOfInformationSerializer, UniversitySerializer,
    FilialSerializer, RegionSerializer, ProgramSerializer, RegisterSerializer, get_dynamic_serializer
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


class RegisterInformationDataListAPIView(ListAPIView):
    """
    ListAPIView to fetch and combine data from multiple models.
    """
    def list(self, request, *args, **kwargs):
        # Check cache first
        # cache_key = "all_data"
        # cached_data = cache.get(cache_key)

        # if cached_data:
        #     return Response(cached_data)

        # Fetch all data from the models
        purposes = list(Purpose.objects.all())
        sources_of_information = list(SourceOfInformation.objects.all())
        universities = list(University.objects.all())
        filials = list(Filial.objects.all())
        regions = list(Region.objects.all())
        programs = list(Program.objects.all())

        # Serialize data for each model dynamically
        data = {
            'purpose': get_dynamic_serializer(Purpose)(purposes, many=True).data,
            'source_of_information': get_dynamic_serializer(SourceOfInformation)(sources_of_information, many=True).data,
            'university': get_dynamic_serializer(University)(universities, many=True).data,
            'filial': get_dynamic_serializer(Filial)(filials, many=True).data,
            'region': get_dynamic_serializer(Region)(regions, many=True).data,
            'program': get_dynamic_serializer(Program)(programs, many=True).data,
        }

        # Cache the result for a specified duration
        # cache.set(cache_key, data, timeout=60 * 10)  # Cache for 10 minutes


        return Response(data)
