from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class PaymentSerializer(serializers.Serializer):
    user_passport_id = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    total_hours = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get_user_full_name(self, obj):
        if obj.get('user_full_name'):
            return obj['user_full_name']
        return f"{obj['user__first_name']} {obj['user__last_name']}"

    def get_user_passport_id(self, obj):
        if obj.get('user_passport_id'):
            return obj['user_passport_id']
        return obj['user__passport_id']
