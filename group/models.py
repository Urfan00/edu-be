from django.db import models
from django.utils.translation import gettext_lazy as _
from services.abstract_models import TimeStampedModel
from django.core.exceptions import ValidationError


class Group(TimeStampedModel):

    class Status(models.TextChoices):
        ACTIVE = 'active', _("Active")          # Aktiv: Qrup hazırda aktivdir və davam edir. Bu, aktiv qrup üçün standart vəziyyətdir.
        PENDING = 'pending', _("Pending")       # Gözlənir: Qrup yaradılıb, lakin hələ başlamamışdır. Bu, müəyyən bir tarixdə başlaması planlaşdırılan gələcək qruplar üçün faydalı ola bilər.
        PAUSED = 'paused', _("Paused")          # Pauza: Qrup müvəqqəti olaraq dayandırılıb (məsələn, tətil və ya fasilələr zamanı), lakin sonradan davam etdirilə bilər. Bu status qrupu tam ləğv etmədən çevikliyə imkan verir.
        COMPLETED = 'completed', _("Completed") # Tamamlandı: Qrup nəzərdə tutulan sonuna çatdı (məsələn, kursun və ya proqramın sonuna), lakin ləğv edilmək və ya müddəti bitmək əvəzinə uğurla tamamlandı.
        CANCELED = 'canceled', _("Canceled")    # Ləğv edildi: Qrup, ola bilsin, az iştirak və ya digər səbəblərə görə vaxtından əvvəl ləğv edildi.
        EXPIRED = 'expired', _("Expired")       # Müddəti bitdi: Qrup rəsmi şəkildə tamamlanmadan planlaşdırılan bitmə tarixini keçdi.
        ARCHIVED = 'archived', _("Archived")    # Arxivləşdirilmiş: Qrup artıq aktiv deyil və ya göstərilmir, lakin tarix və ya qeydlərin aparılması məqsədləri üçün sistemdə qalır.

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_("Status"),
        help_text=_("Current status of the group. It can be Active, Pending, Paused, Completed, Canceled, Expired, or Archived.")
    )
    group_name = models.CharField(
        verbose_name=_("Group Name"),
        max_length=150,
        unique=True
    )
    teacher_passport_id = models.CharField(
        max_length=20,
        verbose_name=_("Teacher Passport ID"),
        help_text=_("The passport ID of the teacher.")
    )
    teacher_full_name = models.CharField(
        max_length=150,
        verbose_name=_("Teacher Full Name"),
        help_text=_("The full name of the teacher."),
        blank=True,
        null=True
    )
    mentor_passport_id = models.CharField(
        max_length=20,
        verbose_name=_("Mentor Passport ID"),
        help_text=_("The passport ID of the mentor."),
        blank=True,
        null=True
    )
    mentor_full_name = models.CharField(
        max_length=150,
        verbose_name=_("Mentor Full Name"),
        help_text=_("The full name of the mentor."),
        blank=True,
        null=True
    )
    start_date = models.DateField(
        verbose_name=_("Start Date"),
    )
    end_date = models.DateField(
        verbose_name=_("End Date"),
        blank=True,
        null=True
    )
    group_salary_for_teacher = models.DecimalField(
        verbose_name=_("Group Salary for Teacher"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("The total salary paid to the teacher for this group.")
    )
    per_student_salary_for_teacher = models.DecimalField(
        verbose_name=_("Per Student Salary for Teacher"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("The salary paid to the teacher per student for this group.")
    )

    def clean(self):
        """
        Custom validation to ensure at least one salary field is filled.
        """
        if not self.group_salary_for_teacher and not self.per_student_salary_for_teacher:
            raise ValidationError(
                _("At least one of 'Group Salary for Teacher' or 'Per Student Salary for Teacher' must be filled.")
            )

    def save(self, *args, **kwargs):
        """
        Override save to call the clean method for validation.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class UserGroup(TimeStampedModel):

    class Status(models.TextChoices):
        ACTIVE = 'active', _("Active")                  # Aktiv: Tələbə qrupda hazırda aktivdir və davam edir.
        GRADUATED = 'graduated', _("Graduated")         # Məzun olub: Tələbə proqramı və ya kursu uğurla başa vurub.
        TRANSFERRED = 'transferred', _("Transferred")   # Köçürüldü: Tələbə başqa qrupa köçürüldü.
        DROPPED_OUT = 'dropped_out', _("Dropped Out")   # Kursdan ayrılıb: Tələbə kursu bitirməmiş qrupdan ayrıldı.

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_("Status"),
        help_text=_("Current status of the student's participation. It can be Graduated, Dropped Out, Transferred or Active.")
    )
    student_passport_id = models.CharField(
        max_length=20,
        verbose_name=_("Student Passport ID"),
        help_text=_("The passport ID of the student.")
    )
    student_full_name = models.CharField(
        max_length=150,
        verbose_name=_("Student Full Name"),
        help_text=_("The full name of the student."),
        blank=True,
        null=True
    )
    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        related_name="user_groups",
        verbose_name=_("Group")
    )
    average = models.DecimalField(
        verbose_name=_("Average"),
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.student_full_name}'s {self.group} group"

    class Meta:
        verbose_name = _("User Group")
        verbose_name_plural = _("User Groups")
        constraints = [
            models.UniqueConstraint(fields=['student_passport_id', 'group'], name='unique_student_passport_group')
        ]
