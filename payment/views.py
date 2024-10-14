from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .serializers import PaymentSerializer
from .models import Payment, PaymentHistory



class PaymentListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):

        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        if month is not None and (not month.isdigit() or not (1 <= int(month) <= 12)):
            raise ValidationError({"month": _("Month must be a valid number between 1 and 12.")})

        if year is not None and not year.isdigit():
            raise ValidationError({"year": _("Year must be a valid number.")})

        if month and year:
            self.queryset = PaymentHistory.objects.filter(
                start_date__year=year,
                start_date__month=month
            ).values('user_full_name', 'user_passport_id').annotate(
                total_hours=Sum('hours_worked'),
                total_price=Sum('total_price')
            )
        else:
            self.queryset = Payment.objects.values('user__passport_id', 'user__first_name', 'user__last_name').annotate(
                    total_hours=Sum('hours'),
                    total_price=Sum('total_price')
                )

        return super().get_queryset()

