from django.db import models
from django.utils.translation import gettext_lazy as _


from identity.models import User
from services.abstract_models import TimeStampedModel


class Group(TimeStampedModel):
    group_name = models.CharField(
        verbose_name=_("Group Name"),
        max_length=150,
        unique=True
    )
    teacher = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="group_teachers",
        limit_choices_to={"user_type": "teacher"},
        verbose_name=_("Teacher")
    )
    operator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="group_operators",
        limit_choices_to={"user_type": "operator"},
        verbose_name=_("Operator")
    )
    is_active = models.BooleanField(
        verbose_name=_("Is Active"),
        default=True,
    )
    start_date = models.DateField(
        verbose_name=_("Start Date"),
    )
    end_date = models.DateField(
        verbose_name=_("End Date"),
        blank=True,
        null=True
    )

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class UserGroup(TimeStampedModel):
    student = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="group_students",
        limit_choices_to={"user_type": "student"},
        verbose_name=_("Student")
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
    )

    def __str__(self):
        return f"{self.student.get_full_name()}'s {self.group} group"

    class Meta:
        verbose_name = _("User Group")
        verbose_name_plural = _("User Groups")
