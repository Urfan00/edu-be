from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Count, Q
from datetime import datetime
from attendance.models import Attendance
from group.models import Group


class TeacherSalaryView(CreateAPIView):
    """
    Generic view to calculate aggregated teacher salaries for a specific month and year.
    """

    def create(self, request, *args, **kwargs):
        # Extract POST data
        teacher_passport_ids = request.data.get("teacher_passport_ids", None)
        month = request.data.get("month")
        year = request.data.get("year")

        # Validate inputs
        if not month or not year:
            raise ValidationError({"error": "Both 'month' and 'year' are required."})

        try:
            month = int(month)
            year = int(year)
            if not (1 <= month <= 12):
                raise ValueError
        except ValueError:
            raise ValidationError({"error": "Invalid 'month' or 'year'. Month must be 1-12."})

        # Define the date range
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        # Filter groups based on teacher_passport_ids (if provided)
        groups = Group.objects.filter(status=Group.Status.ACTIVE).all()
        if teacher_passport_ids:
            groups = groups.filter(teacher_passport_id__in=teacher_passport_ids)

        # Initialize teacher salary aggregation
        teacher_salary_aggregation = {}

        for group in groups:
            # Filter attendance for the group in the specified month and year
            attendance_queryset = Attendance.objects.filter(
                user_group__group=group,
                date__gte=start_date,
                date__lt=end_date,
            )

            # Aggregate attendance for the group
            attendance_summary = attendance_queryset.aggregate(
                total_absent=Count("id", filter=Q(status="absent")),
                total_present=Count("id", filter=Q(status="present")),
                total_late=Count("id", filter=Q(status="late")),
                total_excused=Count("id", filter=Q(status="excused")),
            )

            # Count the attendance status for each student
            student_attendance = (
                attendance_queryset
                .values("user_group__student_passport_id")
                .annotate(
                    total_absent=Count("id", filter=Q(status="absent")),
                    total_present=Count("id", filter=Q(status="present")),
                    total_late=Count("id", filter=Q(status="late")),
                    total_excused=Count("id", filter=Q(status="excused"))
                )
            )

            valid_attendance_count = 0
            total_students = student_attendance.count()
            for student in student_attendance:
                total_absent = student["total_absent"]
                total_present = student["total_present"]
                total_late = student["total_late"]
                total_excused = student["total_excused"]

                # If a student has 3 or more absences
                if total_absent >= 3:
                    # Only consider first 2 absences and all present sessions
                    valid_student_attendance = 2 + total_present + total_late + total_excused
                else:
                    # Otherwise, consider all sessions
                    valid_student_attendance = total_present + total_absent + total_late + total_excused

                # Add the valid attendance for this student to the group-level count
                valid_attendance_count += valid_student_attendance

            # Calculate the total salary for the group
            group_salary = group.group_salary_for_teacher or 0
            per_student_salary = group.per_student_salary_for_teacher or 0
            total_per_student_salary = per_student_salary * valid_attendance_count
            total_salary = group_salary + total_per_student_salary

            # Add detailed group information
            group_details = {
                "group_name": group.group_name,
                "group_salary": group_salary,
                "per_student_salary": per_student_salary,
                "total_students": total_students,
                "valid_attendance_count": valid_attendance_count,
                "total_per_student_salary": total_per_student_salary,
                "group_total_salary": total_salary,
                "attendance_summary": {
                    "total_absent": attendance_summary["total_absent"],
                    "total_present": attendance_summary["total_present"],
                    "total_late": attendance_summary["total_late"],
                    "total_excused": attendance_summary["total_excused"],
                },
            }

            # Aggregate salary by teacher
            if group.teacher_passport_id not in teacher_salary_aggregation:
                teacher_salary_aggregation[group.teacher_passport_id] = {
                    "teacher_name": group.teacher_full_name,
                    "teacher_passport_id": group.teacher_passport_id,
                    "month": month,
                    "year": year,
                    "total_teacher_salary": total_salary,
                    "groups": [group_details],  # Add the group's details
                }
            else:
                teacher_salary_aggregation[group.teacher_passport_id]["total_teacher_salary"] += total_salary
                teacher_salary_aggregation[group.teacher_passport_id]["groups"].append(group_details)

        return Response(list(teacher_salary_aggregation.values()))
