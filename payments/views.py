from rest_framework import APIView, status
from rest_framework.response import Response
from .models import Payment, Transaction, PaymentMethod
from .serializers import PaymentSerializer, TransactionSerializer
from orders.models import Order

# Create payment view
class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        order_id = data.get('order_id')
        user = request.user
        payment_method_id = data.get('payment_method_id')
        
        try:
            order = Order.objects.get(id=order_id, user=user)
            payment_method = payment_method.objects.get(id=payment_method_id)
            
            payment = Payment.objects.create(
                user=user,
                order=order,
                amount=order.total_amount,
                payment_method=payment_method,
            )
            # Serialize the payment and return the response
            payment_serializer = PaymentSerializer(payment)
            return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or does not belong to the user.'}, status=status.HTTP_404_NOT_FOUND)
        except PaymentMethod.DoesNotExist:
            return Response({'error': 'Payment method not found.'}, status=status.HTTP_404_NOT_FOUND) 


# Process payment view
class ProcessPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        payment_id = data.get('payment_id')
        transaction_reference = data.get('transaction_reference')
        payment_gateway = data.get('payment_gateway')
        amount = data.get('amount')
        
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
            # I will implement payment integration here later
            # For now, let's assume the payment is always successful
            
            # Create a transaction record
            transaction = Transaction.objects.create(
                payment=payment,
                transaction_id=transaction_reference,
                amount=payment.amount,
                status='completed', # assuming success for now
                payment_gateway_response={'message': 'Payment processed successfully'} # mock response
            )
            
            # Update payment status
            payment.status = 'completed'
            payment.save() 
            
            # Serialize and return the transaction response
            transaction_serializer = TransactionSerializer(transaction)
            return Response(transaction_serializer.data, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND) 


# Payment status view
class PaymentStatusView(APIView):
    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get('payment_id')
        
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
            payment_serializer = PaymentSerializer(payment)
            return Response(payment_serializer.data, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND) 
