from django.db import models
from django.utils.translation import gettext_lazy as _
from identity.models import User
from services.abstract_models import TimeStampedModel
from django.core.validators import RegexValidator



class Purpose(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Purpose Name",
        help_text="Enter a short, descriptive name for the purpose."  # Tooltip-like help in admin/forms
    )

    class Meta:
        verbose_name = _("Purpose")
        verbose_name_plural = _("Purposes")
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class SourceOfInformation(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Source Name",  # Descriptive label in admin/forms
        help_text="Enter the name of the information source."  # Tooltip-like help in admin/forms
    )

    class Meta:
        verbose_name = _("Source of Information")
        verbose_name_plural = _("Sources of Information")
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class University(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="University Name",
        help_text="Enter the full name of the university."
    )

    class Meta:
        verbose_name = _("University")
        verbose_name_plural = _("Universities")
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Filial(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Filial Name",
        help_text="Enter the name of the filial (branch)."
    )

    class Meta:
        verbose_name = _("Filial")
        verbose_name_plural = _("Filials")
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Region(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Region Name",
        help_text="Enter the name of the region."
    )

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Program(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Program Name",
        help_text="Enter the name of the program."
    )

    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programs")
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Register(TimeStampedModel):

    class GenderChoices(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        OTHER = "O", _("Other")

    class LessonType(models.TextChoices):
        ONLINE = "online", _("Online")
        OFFLINE = "offline", _("Offline")

    class Status(models.TextChoices):
        ONHOLD = 'on_hold', _("On Hold")
        TEST = 'test', _("Test")
        ACTIVE = 'active', _("Active")
        DEACTIVE = 'deactive', _("Deactive")

    first_name = models.CharField(
        _("first name"),
        max_length=150,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
    )
    father_name = models.CharField(
        verbose_name=_("Father name"),
        max_length=150,
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True
    )
    passport_id = models.CharField(
        verbose_name=_("Passport ID"),
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]+$',
                message=_("Passport ID must contain only letters and numbers.")
            )
        ],
        help_text=_("Enter a valid passport ID with letters and numbers.")
    )
    phone_number_1 = models.CharField(
        verbose_name=_("Phone number 1"),
        max_length=50,
        help_text=_(
            "Enter the phone number of the user. For example: +994123456789."
        )
    )
    phone_number_2 = models.CharField(
        verbose_name=_("Phone number 2"),
        max_length=50,
        help_text=_(
            "Enter the phone number of the user. For example: +994123456789."
        )
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE
    )
    lesson_type = models.CharField(
        verbose_name=_("Lesson Type"),
        max_length=10,
        choices=LessonType.choices,
        default=LessonType.OFFLINE
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=15,
        choices=Status.choices,
        default=Status.ONHOLD,
        help_text=_("Current status of the payment.")
    )
    purpose = models.CharField(
        max_length=255,
        verbose_name=_("Purpose"),
        help_text=_("Enter the purpose for registration.")
    )
    source_of_information = models.CharField(
        max_length=255,
        verbose_name=_("Source of Information"),
        help_text=_("Enter the source of information.")
    )
    university = models.CharField(
        max_length=255,
        verbose_name=_("University"),
        help_text=_("Enter the university name.")
    )
    filial = models.CharField(
        max_length=255,
        verbose_name=_("Filial"),
        help_text=_("Enter the filial (branch) name.")
    )
    region = models.CharField(
        max_length=255,
        verbose_name=_("Region"),
        help_text=_("Enter the region name.")
    )
    program = models.CharField(
        max_length=255,
        verbose_name=_("Program"),
        help_text=_("Enter the program name.")
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = _("Registration")
        verbose_name_plural = _("Registrations")
        ordering = ['-created_at']
