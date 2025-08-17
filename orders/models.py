from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

# Class to represent orders
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),    
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.email} - {self.status}"
    
    def update_total_amount(self):
        """ Update the total amount of the order based on related OrderItems """
        total = sum(item.total_price for item in self.orderitem_set.all())
        self.total_amount = total
        self.save()
        
    def save(self, *args, **kwargs):
        """ Override save method to update total_amount before saving """
        if self.pk:
            self.update_total_amount() # Update total amount when the order is being saved/updated
        super().save(*args, **kwargs)        
    
    
# Class to represent order items
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"  
    
    
    def save(self, *args, **kwargs):
        """ Override save method to calculate total_price before saving """
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.order.update_total_amount() # After saving the order item, update the order's total amount 
    
