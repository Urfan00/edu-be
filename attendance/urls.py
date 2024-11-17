from django.urls import path
from .views import AttendanceListCreateView


app_name = "attendance"


urlpatterns = [
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance'),
]
