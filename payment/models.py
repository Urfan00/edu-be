from django.db import models
from django.utils.translation import gettext_lazy as _
from services.abstract_models import TimeStampedModel
from identity.models import User


class Payment(TimeStampedModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("User")
    )
    hours = models.PositiveIntegerField(
        verbose_name=_("Hours"),
        help_text=_("The number of hours worked.")
    )
    start_date = models.DateTimeField(
        verbose_name=_("Start Date and Time"),
        help_text=_("The start date and time of the period for this payment history.")
    )
    end_date = models.DateTimeField(
        verbose_name=_("End Date and Time"),
        help_text=_("The end date and time of the period for this payment history."),
        null=True,
        blank=True
    )
    price_per_hour = models.DecimalField(
        verbose_name=_("Price Per Hour (AZN)"),
        max_digits=10,  # Example: 9999999.999₼
        decimal_places=3,
        help_text=_("Price per hour in AZN, e.g. 0.001₼")
    )
    total_price = models.DecimalField(
        verbose_name=_("Total Price (AZN)"),
        max_digits=10,  # Example: 9999999.99₼
        decimal_places=2,
        help_text=_("Total price calculated based on hours * price per hour.")
    )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment of {self.total_price} AZN for {self.user.get_full_name()}"


class PaymentHistory(TimeStampedModel):
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
    start_date = models.DateTimeField(
        verbose_name=_("Start Date and Time"),
        help_text=_("The start date and time of the period for this payment history.")
    )
    end_date = models.DateTimeField(
        verbose_name=_("End Date and Time"),
        help_text=_("The end date and time of the period for this payment history.")
    )
    hours_worked = models.PositiveIntegerField(
        verbose_name=_("Hours Worked"),
        help_text=_("The number of hours worked during the specified period.")
    )
    hourly_rate = models.DecimalField(
        verbose_name=_("Hourly Rate (AZN)"),
        max_digits=10,  # Example: 9999999.999₼
        decimal_places=3,
        help_text=_("The hourly rate in AZN for this payment.")
    )
    total_price = models.DecimalField(
        verbose_name=_("Total Price (AZN)"),
        max_digits=10,  # Example: 9999999.99₼
        decimal_places=2,
        help_text=_("Total payment amount for the hours worked.")
    )

    class Meta:
        verbose_name = _("Payment History")
        verbose_name_plural = _("Payment Histories")
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment history for {self.user_passport_id} ({self.start_date} - {self.end_date})"
