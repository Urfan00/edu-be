from django.db import models
from django.utils.translation import gettext_lazy as _
from group.models import UserGroup
from services.abstract_models import TimeStampedModel


class Attendance(TimeStampedModel):
    class Status(models.TextChoices):
        PRESENT = 'present', _("Present")       # İştirak: Tələbə dərsdə iştirak edib.
        ABSENT = 'absent', _("Absent")          # Qeybdə: Tələbə dərsdə iştirak etməyib.
        LATE = 'late', _("Late")                # Gecikmiş: Tələbə dərsə gecikib.
        EXCUSED = 'excused', _("Excused")       # İcazəli: Tələbə məlum səbəblərdən dərsdə iştirak etməyib.

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        verbose_name=_("Status"),
        help_text=_("The attendance status of the student for this session. Options include Present, Absent, Late, or Excused.")
    )
    date = models.DateField(
        verbose_name=_("Date"),
        help_text=_("The date of the class or session for which attendance is being recorded.")
    )
    user_group = models.ForeignKey(
        to=UserGroup,
        on_delete=models.CASCADE,
        related_name="attendance_user_group",
        verbose_name=_("User Group"),
        help_text=_("The user group to which the attendance record belongs.")
    )


    def __str__(self):
        return f"{self.user_group.student_full_name} - {self.date} - {self.status}"

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendance Records")
        constraints = [
            models.UniqueConstraint(fields=['date', 'user_group'], name='unique_attendance_per_user_group_and_date')
        ]
