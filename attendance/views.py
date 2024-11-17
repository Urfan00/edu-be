from rest_framework.generics import ListCreateAPIView
from .models import Attendance
from .serializers import AttendanceCreateSerializer, AttendanceListSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError



class AttendanceListCreateView(ListCreateAPIView):
    """
    API view for listing & creating attendance records.
    """
    queryset = Attendance.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_group__group__group_name', 'user_group__student_full_name', 'status', 'date']
    search_fields = ['user_group__student_full_name', 'user_group__group__group_name']
    ordering_fields = ['date']
    ordering = ['-date']

    def get_serializer_class(self):
        """
        Use different serializers for listing and creating.
        """
        if self.request.method == 'POST':
            return AttendanceCreateSerializer
        return AttendanceListSerializer

    def get_queryset(self):
        """
        Override to enforce required query parameters for listing attendance.
        """
        queryset = super().get_queryset()

        # Get query parameters
        group_name = self.request.query_params.get('group_name')
        month = self.request.query_params.get('month')

        # Validate that required parameters are provided
        if not group_name:
            raise ValidationError({"detail": "The 'group_name' query parameter is required."})
        if not month:
            raise ValidationError({"detail": "The 'month' query parameter is required."})

        # Filter queryset by group name and month
        queryset = queryset.filter(user_group__group__group_name=group_name)

        # Filter by month (assuming the date field is used to filter the month)
        queryset = queryset.filter(date__month=month)

        return queryset
