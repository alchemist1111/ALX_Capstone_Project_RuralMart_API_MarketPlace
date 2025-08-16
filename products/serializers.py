from rest_framework import serializers
from .models import Category, Product, Cart, CartItem
from .cart_utils import calculate_cart_total


# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

# Product serializer
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'category', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display user as a string (for authenticated users)
    total = serializers.SerializerMethodField()  # Calculate total for the cart
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def get_total(self, obj):
        return calculate_cart_total(obj)  # This function calculates the total price of the cart
        
        
# CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), read_only=True) # Nested cart serializer
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), read_only=True) # Nested product serializer
    quantity = serializers.IntegerField(min_value=1) # Quantity should always be positive integer
    
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'added_at'] 
        read_only_fields = ['id', 'added_at'] 
        
    def validate_quantity(self, value):
        """Quantity should always be a positive integer."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value
                                 