from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

# OrderItem Serializer (for individual items in an order)
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # Calculated total_price
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['total_price'] 
    
    def validate_quantity(self, value):
        """ Quantity should always be a positive integer """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    
    def validate_unit_price(self, value):
        """ Ensure unit_price is positive and valid """
        if value <= 0:
            raise serializers.ValidationError("Unit price must be greater than zero.")
        return value
    
# Order Serializer (for representing the entire order with items)
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display user email (or other identifier)
    order_items = OrderItemSerializer(many=True, read_only=True)  # Nested OrderItems as part of the order
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # Total amount of the order
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'status', 'total_amount', 'order_items']
        read_only_fields = ['total_amount', 'order_items']  # Make total_amount and order_items read-only
    
    def create(self, validated_data):
        """ Overriding create method to handle nested order items """
        # Extract order items from validated data
        order_items_data = validated_data.pop('order_items', [])
        
        # Create the order instance
        order = Order.objects.create(**validated_data)
        
        # Create order items and associate them with the newly created order
        for item_data in order_items_data:
            item_data['order'] = order  # Associate the item with the correct order
            OrderItem.objects.create(**item_data)
        return order
    
    def update(self, instance, validated_data):
        """ Overriding update method to handle updates to nested order items """
        order_items_data = validated_data.pop('order_items', [])
        
        # Update basic order details
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        
        # Update order items
        for item_data in order_items_data:
            # Assuming the item already exists, update it, otherwise create new ones
            product = item_data.get('product', None)
            if product:
                order_item, created = OrderItem.objects.get_or_create(order=instance, product=product)
                order_item.quantity = item_data.get('quantity', order_item.quantity)
                order_item.unit_price = item_data.get('unit_price', order_item.unit_price)
                order_item.total_price = order_item.quantity * order_item.unit_price  # Recalculate total price
                order_item.save()
                
        # Recalculate the total amount for the order after updating the items
        instance.update_total_amount()
        return instance        