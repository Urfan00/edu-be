from django.contrib import admin
from .models import Payment, UserPayment
from import_export.admin import ImportExportModelAdmin


@admin.register(UserPayment)
class UserPaymentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user_full_name', 'user_passport_id', 'user_type', 'price_per_hour', 'end_date', 'created_at', 'updated_at')
    list_filter = ('user_type', 'end_date', 'created_at')
    search_fields = ('user_full_name', 'user_passport_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user_full_name', 'user_passport_id', 'status', 'month', 'total_price', 'total_hours', 'created_at', 'updated_at')
    list_filter = ('status', 'month', 'created_at')
    search_fields = ('user_full_name', 'user_passport_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
