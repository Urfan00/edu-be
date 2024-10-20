from django.db import models
from django.utils.translation import gettext_lazy as _
from identity.models import User
from services.abstract_models import TimeStampedModel



class UserPayment(TimeStampedModel):
    user_passport_id = models.CharField(
        verbose_name=_("User Passport ID"),
        max_length=15,
        help_text=_("Passport ID of the user for this payment record.")
    )
    user_full_name = models.CharField(
        verbose_name=_("User Full Name"),
        max_length=255,
        help_text=_("Full name of the user for this payment record.")
    )
    user_type = models.CharField(
        verbose_name=_("User Type"),
        max_length=20,
        choices=User.UserTypeChoices.choices,
        help_text=_("Type of user (e.g., Student, Teacher, etc.) for this payment record.")
    )
    price_per_hour = models.DecimalField(
        verbose_name=_("Price Per Hour (AZN)"),
        max_digits=10,
        decimal_places=3,
        help_text=_("Hourly rate for the payment, in AZN. Example: 15.000₼.")
    )
    end_date = models.DateTimeField(
        verbose_name=_("End Date and Time"),
        help_text=_("End date and time for the payment period."),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("User Payment")
        verbose_name_plural = _("User Payments")
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for {self.user_full_name} ({self.user_passport_id}) - {self.price_per_hour} AZN/hour"


class Payment(TimeStampedModel):
    class Status(models.TextChoices):
        IN_CALCULATION = 'in_calculation', _("In Calculation")
        PENDING = 'pending', _("Pending")
        PAID = 'paid', _("Paid")
        OVERDUE = 'overdue', _("Overdue")
        FAILED = 'failed', _("Failed")
        CANCELED = 'canceled', _("Canceled")

    class Month(models.TextChoices):
        JANUARY = 'january', _("January")
        FEBRUARY = 'february', _("February")
        MARCH = 'march', _("March")
        APRIL = 'april', _("April")
        MAY = 'may', _("May")
        JUNE = 'june', _("June")
        JULY = 'july', _("July")
        AUGUST = 'august', _("August")
        SEPTEMBER = 'september', _("September")
        OCTOBER = 'october', _("October")
        NOVEMBER = 'november', _("November")
        DECEMBER = 'december', _("December")

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=15,
        choices=Status.choices,
        default=Status.IN_CALCULATION,
        help_text=_("Current status of the payment.")
    )
    month = models.CharField(
        verbose_name=_("Month"),
        max_length=15,
        choices=Month.choices,
        default=Month.JANUARY,
        help_text=_("The month the payment is associated with.")
    )
    user_passport_id = models.CharField(
        verbose_name=_("User Passport ID"),
        max_length=15,
        help_text=_("Passport ID of the user for the payment history.")
    )
    user_full_name = models.CharField(
        verbose_name=_("User Full Name"),
        max_length=255,
        help_text=_("Full name of the user for the payment history.")
    )
    total_price = models.DecimalField(
        verbose_name=_("Total Price (AZN)"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Total price calculated based on hours * price per hour."),
        null=True,
        blank=True
    )
    total_hours = models.DecimalField(
        verbose_name=_("Hours"),
        max_digits=10,
        decimal_places=2,
        help_text=_("The number of hours worked."),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment of {self.total_price} AZN for {self.user_full_name} ({self.user_passport_id})."
