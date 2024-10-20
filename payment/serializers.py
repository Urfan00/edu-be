from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Payment, UserPayment
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user_full_name', 'user_passport_id', 'status', 'total_price', 'total_hours', 'month']


class UserPaymentModalSerializer(serializers.ModelSerializer):
    hours = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    begin_date = serializers.SerializerMethodField()
    finish_date = serializers.SerializerMethodField()

    class Meta:
        model = UserPayment
        fields = ['id', 'user_full_name', 'user_passport_id', 'user_type', 'price_per_hour', 'begin_date', 'finish_date', 'hours', 'price']

    def get_begin_date(self, obj):
        # Ensure the begin date is within the selected month
        month_start = self.context['month_start']
        return max(obj.created_at, month_start).strftime("%Y-%m-%d %H:%M:%S")

    def get_finish_date(self, obj):
        # Ensure the finish date is within the selected month or handle ongoing roles
        month_end = self.context['month_end']
        if obj.end_date:
            finish_date = min(obj.end_date, month_end)
            # If finish date is exactly midnight of the last day of the month, set to 00:00:00 of the next day
            if finish_date == month_end.replace(hour=0, minute=0, second=0):
                # Move to the next day at 00:00:00
                finish_date = finish_date + timedelta(days=1)
            return finish_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            # Handle ongoing roles (end_date is null)
            return "Ongoing"  # Or use timezone.now() if you want the current date/time for ongoing roles

    def get_hours(self, obj):
        # Get month start and month end from context
        month_start = self.context['month_start']
        month_end = self.context['month_end']
        
        # Calculate begin and finish dates limited to the current month
        begin_date = max(obj.created_at, month_start)
        if obj.end_date:
            finish_date = min(obj.end_date, month_end)
            # Adjust finish_date to 00:00:00 of the next day if it's exactly at midnight of the last day of the month
            if finish_date == month_end.replace(hour=0, minute=0, second=0):
                finish_date = finish_date + timedelta(days=1)
        else:
            # If the role is ongoing, set finish_date to current date, ensure timezone-aware comparison
            finish_date = min(month_end, timezone.now() + timedelta(hours=4))

        # Calculate the time difference between begin_date and finish_date
        delta = finish_date - begin_date
        
        # Convert the delta into hours
        total_hours = delta.total_seconds() / 3600  # Convert seconds to hours
        return Decimal(total_hours)  # Convert to Decimal for precision

    def get_price(self, obj):
        # Calculate the price based on the hours worked and price_per_hour
        hours = self.get_hours(obj)
        return round(hours * obj.price_per_hour, 3)
