import uuid
from django.contrib.auth import get_backends
from django.contrib.auth.models import AbstractBaseUser, Permission
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from identity.managers import CustomUserManager
from services.abstract_models import TimeStampedModel


def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = "get_%s_permissions" % from_name
    for backend in get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions


class Role(TimeStampedModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=150,
        unique=True
    )
    description = models.TextField(
        verbose_name=_("Description"),
        null=True,
        blank=True,
    )
    status = models.BooleanField(
        verbose_name=_("Status"),
        default=True,
    )
    permissions = models.ManyToManyField(
        to=Permission,
        blank=True,
        verbose_name=_("Permissions")
    )

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        OTHER = "O", _("Other")

    class UserTypeChoices(models.TextChoices):
        STUDENT = "student", _("Student")
        PARENT = "parent", _("Parent")
        TEACHER = "teacher", _("Teacher")
        STAFF = "staff", _("Staff")
        DIRECTOR = "director", _("Director")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
    )
    father_name = models.CharField(
        verbose_name=_("Father name"),
        max_length=150,
        blank=True
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
        verbose_name=_("Phone number"),
        max_length=50,
        help_text=_(
            "Enter the phone number 1 of the user. For example: +994123456789."
        )
    )
    phone_number_2 = models.CharField(
        verbose_name=_("Phone number"),
        max_length=50,
        help_text=_(
            "Enter the phone number 2 of the user. For example: +994123456789."
        )
    )
    user_type = models.CharField(
        verbose_name=_("User Type"),
        max_length=20,
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.STUDENT
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE
    )
    profile_image = models.ImageField(
        verbose_name=_("Profile Image"),
        upload_to="profile_images/",
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name=_("Bio"),
        blank=True,
    )
    instagram = models.URLField(
        verbose_name=_("Instagram Profile"),
        blank=True,
        null=True,
        help_text=_("Enter a valid URL for the Instagram profile.")
    )
    facebook = models.URLField(
        verbose_name=_("Facebook Profile"),
        blank=True,
        null=True,
        help_text=_("Enter a valid URL for the Facebook profile.")
    )
    twitter = models.URLField(
        verbose_name=_("Twitter Profile"),
        blank=True,
        null=True,
        help_text=_("Enter a valid URL for the Twitter profile.")
    )
    github = models.URLField(
        verbose_name=_("GitHub Profile"),
        blank=True,
        null=True,
        help_text=_("Enter a valid URL for the GitHub profile.")
    )
    youtube = models.URLField(
        verbose_name=_("YouTube Channel"),
        blank=True,
        null=True,
        help_text=_("Enter a valid URL for the YouTube channel.")
    )
    linkedin = models.URLField(
        verbose_name=_("LinkedIn Profile"),
        blank=True,
        null=True,
        help_text=_("Enter a valid URL for the LinkedIn profile.")
    )
    address = models.CharField(
        verbose_name=_("Address"),
        max_length=255,
        blank=True,
        help_text=_("Enter the user's address.")
    )
    first_time_login = models.BooleanField(
        verbose_name=_("First Time Login"),
        default=True,
        help_text=_(
            "Indicates whether the user is logging in for the first time.")
    )
    roles = models.ManyToManyField(
        to="identity.Role",
        blank=True,
        related_name="users",
        verbose_name=_("Roles"),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_superuser = models.BooleanField(
        verbose_name=_("Superuser"),
        default=False,
        help_text=_("Designates whether this user has all permissions.")
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        """Return True if the user is a superuser, otherwise False."""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Return True if the user has permissions for the app."""
        return self.is_superuser

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"{self.email} - {full_name}"
        return f"{self.email}"

    def get_full_name(self):
        """
            Return the first_name plus the last_name plus the father_name, with a space in between.
            """
        full_name = "%s %s %s" % (
            self.first_name, self.last_name, self.father_name)
        return full_name.strip()

    def get_role_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their roles.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "role")


class AccessToken(models.Model):
    jti = models.CharField(
        verbose_name=_("JTI"),
        max_length=255,
        unique=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="access_tokens",
        verbose_name=_("User")
    )
    token = models.TextField(
        verbose_name=_("Token"),
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
    )
    expires_at = models.DateTimeField(
        verbose_name=_("Expires at"),
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True
    )

    class Meta:
        app_label = "token_blacklist"
        verbose_name = _("Access token")
        verbose_name_plural = _("Access tokens")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.email} - {self.jti}"
