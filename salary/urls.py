from django.urls import path
from salary.views import TeacherSalaryView


app_name = "salary"

urlpatterns = [
    path('teacher_salary/', TeacherSalaryView.as_view(), name='teacher_salary'),

]
