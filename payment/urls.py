from .views import PaymentListView, UserPaymentModalListView
from django.urls import path

app_name = "payment"


urlpatterns = [
    path('payment_list/', PaymentListView.as_view(), name='payment_list'),
    path('payment_modal_list/', UserPaymentModalListView.as_view(), name='payment_modal_list')
]
