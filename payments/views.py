from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment, Transaction, PaymentMethod
from .serializers import PaymentSerializer, TransactionSerializer, PaymentMethodSerializer
from orders.models import Order
from .paystack_service import initialize_payment
from .paystack_service import verify_payment
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create payment view
class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        order_id = data.get('order_id')
        user = request.user
        payment_method_id = data.get('payment_method_id')
        
        if not order_id or not payment_method_id:
           return Response({'error': 'order_id and payment_method_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = Order.objects.get(id=order_id, user=user)
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
            
            # Initialize payment with Paystack
            try:
                payment = initialize_payment(order.total_amount, user.email, order_id)
                if 'error' in payment:
                    return Response({'error': payment['error']}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'Payment initialization failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            
            payment_record = Payment.objects.create(
                user=user,
                order=order,
                amount=order.total_amount,
                payment_method=payment_method,
                status='pending',
                payment_gateway='paystack',
                transaction_reference=payment['data']['reference']
            )
            # Return the URL to redirect the user for payment
            return Response({
                'authorization_url': payment['data']['authorization_url'],
                'transaction_reference': payment['data']['reference'],
                'payment_id': payment_record.id
            }, status=status.HTTP_201_CREATED)
            
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
        
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
            
            # Verify the payment with Paystack
            verification_response = verify_payment(transaction_reference)
            
            if 'error' in verification_response:
                return Response({'error': verification_response['error']}, status=status.HTTP_400_BAD_REQUEST)
            
               # If payment is successful
            if verification_response['data']['status'] == 'success':
                # Update the payment status
                payment.status = 'completed'
                payment.save()
            
                # Create a transaction record
                transaction = Transaction.objects.create(
                    payment=payment,
                    transaction_id=transaction_reference,
                    amount=payment.amount,
                    status='completed',
                    payment_gateway_response=verification_response
                )
            
                # Serialize and return the transaction response
                transaction_serializer = TransactionSerializer(transaction)
                return Response(transaction_serializer.data, status=status.HTTP_200_OK)
            else:
                payment.status = 'failed'
                payment.save()
                return Response({'error': 'Payment verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
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
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

# Webhook for Paystack to notify your server of payment events
@method_decorator(csrf_exempt, name='dispatch')
class PayStackWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract relevant data from the request payload
        payment_reference = request.data.get('data', {}).get('reference')
        payment_status = request.data.get('data', {}).get('status')
        
        if not payment_reference or not payment_status:
            return Response({'error': 'Invalid webhook data'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Find the payment record using the reference
            payment = Payment.objects.get(transaction_reference=payment_reference)
            
            # Update the payment status based on Paystack's response
            if payment_status == 'success':
                payment.status = 'completed'
            elif payment_status == 'failed':
                payment.status = 'failed'
            else:
                payment.status = 'pending'
            
            payment.save()
            
            return Response({'message': 'Payment status updated successfully.'}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND) 


# Payment method view
class PaymentMethodView(APIView):
    def get(self, request, *args, **kwargs):
        # Ensure the user is authenticated and fetch only their payment methods
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        payment_methods = PaymentMethod.objects.filter(user=request.user)
        serializer = PaymentMethodSerializer(payment_methods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Add the user to the data before saving
        data = request.data
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                    
