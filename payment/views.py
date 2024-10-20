from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Payment, UserPayment
from .serializers import PaymentSerializer, UserPaymentModalSerializer
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from decimal import Decimal
from django.db.models import Q



class PaymentListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):

        current_month = timezone.now().strftime('%B').lower()

        month = self.request.query_params.get('month')
        status = self.request.query_params.get('status')

        if month and status:
            if month not in dict(Payment.Month.choices).keys():
                raise ValidationError({"month": _("Month must be one of the valid values: 'january', 'february', etc.'")})

            if status not in dict(Payment.Status.choices).keys():
                raise ValidationError({"status": _("Status must be one of the valid values: 'in_calculation', 'pending', etc.'")})

            return Payment.objects.filter(month=month, status=status)

        if not month and not status:
            pending_payments = Payment.objects.filter(status=Payment.Status.PENDING)

            if pending_payments.exists():
                self.queryset = pending_payments
                return super().get_queryset()

            in_calculation_payments = Payment.objects.filter(status=Payment.Status.IN_CALCULATION, month=current_month)
            self.queryset = in_calculation_payments
            return super().get_queryset()

        self.queryset = Payment.objects.all()

        if month:
            if month not in dict(Payment.Month.choices).keys():
                raise ValidationError({"month": _("Month must be one of the valid values: 'january', 'february', etc.'")})
            self.queryset = self.queryset.filter(month=month)

        if status:
            if status not in dict(Payment.Status.choices).keys():
                raise ValidationError({"status": _("Status must be one of the valid values: 'in_calculation', 'pending', etc.'")})
            self.queryset = self.queryset.filter(status=status)

        return super().get_queryset()


class UserPaymentModalListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPaymentModalSerializer

    def get_queryset(self):
        passport_id = self.request.query_params.get('passport_id')
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')

        if not passport_id:
            raise ValidationError({"detail": _("Passport ID is required.")})
        if not year or not month:
            raise ValidationError({"detail": _("Year and Month are required.")})

        # Parse the year and month into a start and end date
        try:
            month_start = make_aware(datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d"))
            # Calculate the end of the month (get the last day of the month)
            next_month = (month_start.month % 12) + 1
            next_month_start = month_start.replace(month=next_month, day=1)
            month_end = next_month_start - timedelta(days=1)  # Last day of the current month
        except ValueError:
            raise ValidationError({"detail": _("Invalid year or month format. Please use YYYY for year and MM for month.")})

        # Filter for records that overlap with the selected month
        queryset = UserPayment.objects.filter(
            Q(user_passport_id=passport_id) & 
            (
                # End date is after the start of the month OR ongoing roles (null end_date)
                Q(end_date__gte=month_start) | Q(end_date__isnull=True)
            ) &
            Q(created_at__lte=month_end)  # Created date should be before the end of the month
        )

        if not queryset.exists():
            raise ValidationError({"detail": "No payment data found for this passport ID in the given month."})

        return queryset

    def get_serializer_context(self):
        # Add month_start and month_end to serializer context for date handling
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')

        try:
            month_start = make_aware(datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d"))
            next_month = (month_start.month % 12) + 1
            next_month_start = month_start.replace(month=next_month, day=1)
            month_end = next_month_start - timedelta(days=1)
        except ValueError:
            raise ValidationError({"detail": _("Invalid year or month format. Please use YYYY for year and MM for month.")})

        return {
            'month_start': month_start,
            'month_end': month_end,
        }
