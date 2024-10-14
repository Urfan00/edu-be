from .views import PaymentListView
from django.urls import path

app_name = "payment"


urlpatterns = [
    path('payment_list/', PaymentListView.as_view(), name='payment_list')
]
