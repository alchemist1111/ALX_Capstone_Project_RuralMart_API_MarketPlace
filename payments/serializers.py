from rest_framework import serializers
from .models import Payment, PaymentMethod, Transaction


# Serializer for PaymentMethod
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']
        
# Serializer for Payment
class PaymentSerializer(serializers.ModelSerializer):
    payment_method = PaymentMethodSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'payment_method', 'status', 'payment_date', 'transaction_reference', 'payment_gateway']
        read_only_fields = ['user', 'order', 'payment_date']
        
# Serializer for Transaction
class TransactionSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'payment', 'amount', 'status', 'transaction_date', 'payment_gateway_response']
        read_only_fields = ['transaction_date']
                        