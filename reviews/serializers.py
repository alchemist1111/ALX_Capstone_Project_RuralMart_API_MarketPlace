from rest_framework import serializers
from .models import Review
from accounts.serializers import UserSerializer
from products.serializers import ProductSerializer
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested user serializer
    product = ProductSerializer(read_only=True)  # Nested product serializer
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(allow_blank=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'product', 'created_at']
        
    def create(self, validated_data):
        # Automatically assign the logged-in user to the review
        request = self.context.get('request')
        user = request.user if request else None
        validated_data['user'] = user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Prevent changing the user and product on update
        validated_data.pop('user', None)
        validated_data.pop('product', None)
        return super().update(instance, validated_data)    
    
    # Validate that a user cannot review the same product more than once
    def validate(self, data):
        user = self.context.get('request').user
        product = data.get('product')
        
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        return data