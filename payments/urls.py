from django.urls import path
from .views import CreatePaymentView, ProcessPaymentView, PaymentStatusView

urlpatterns = [
    # Payment method urls
    
    # Payment URLs
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('process-payment/', ProcessPaymentView.as_view(), name='process-payment'),
    path('payment-status/<int:payment_id>/', PaymentStatusView.as_view(), name='payment-status'),
]
