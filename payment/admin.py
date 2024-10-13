from django.contrib import admin
from .models import Payment, PaymentHistory


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'hours', 'price_per_hour', 'total_price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'user__passport_id')
    readonly_fields = ('created_at', 'updated_at')

    # Automatically calculate total price based on hours and price per hour
    def save_model(self, request, obj, form, change):
        if not obj.total_price:
            obj.total_price = obj.hours * obj.price_per_hour
        super().save_model(request, obj, form, change)


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'user_passport_id', 'start_date', 'end_date', 'hours_worked', 'hourly_rate', 'total_price', 'created_at', 'updated_at')
    list_filter = ('start_date', 'end_date', 'created_at', 'updated_at')
    search_fields = ('user_full_name', 'user_passport_id')
    readonly_fields = ('created_at', 'updated_at')
