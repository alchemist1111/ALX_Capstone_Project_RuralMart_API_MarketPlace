from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

# Class to represent a product review
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # Rating from 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
               constraints = [
                      models.UniqueConstraint(fields=['user', 'product'], name='unique_review')
                    ] # Ensure one review per user per product
               
               ordering = ['-created_at']
        
    def __str__(self):
        return f'Review by: {self.user.first_name} {self.user.last_name} for {self.product.name} - Rating: {self.rating}'    
