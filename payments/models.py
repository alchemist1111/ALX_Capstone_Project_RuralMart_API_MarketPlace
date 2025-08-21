from django.db import models
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()

# Payment method model
class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
# Payment model
class Payment(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ] 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status_choices, default='pending') 
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    payment_gateway = models.CharField(max_length=255, blank=True, null=True) # eg stripe, mpesa, or paypal
    
    def __str__(self):
        return f"Payment for Order {self.order.id} by {self.user.email}"
    
    def is_successful(self):
        return self.status == 'completed' 
    
    
# Transaction model
class Transaction(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_gateway_response = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id} for Payment {self.payment.id}"    
