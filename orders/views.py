from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from django.shortcuts import get_object_or_404


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access orders

    def get_queryset(self):
        """
        This view should return a list of all the orders for the currently authenticated user.
        """
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Override to set the user for the order"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Custom action to add an item to the order"""
        order = self.get_object()
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")
        unit_price = request.data.get("unit_price")

        # Ensure the product exists
        product = get_object_or_404(Product, pk=product_id)
        
        # Create order item
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=unit_price
        )

        # Update the order's total amount
        order.update_total_amount()

        return Response(OrderSerializer(order).data)  # Return the updated order

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """Custom action to remove an item from the order"""
        order = self.get_object()
        item_id = request.data.get("item_id")

        # Ensure the order item exists
        order_item = get_object_or_404(OrderItem, pk=item_id, order=order)
        order_item.delete()

        # Update the order's total amount
        order.update_total_amount()

        return Response(OrderSerializer(order).data)  # Return the updated order


# OrderItem ViewSet
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the order items for the current user's orders.
        """
        return OrderItem.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        """Override to set the order for the order item"""
        order = get_object_or_404(Order, pk=self.kwargs['order_pk'])
        serializer.save(order=order)
        
        # Update the order's total amount after adding the item
        order.update_total_amount()

    def perform_update(self, serializer):
        """Override to recalculate the total price after updating an item"""
        instance = serializer.save()

        # Update the order's total amount after the update
        instance.order.update_total_amount()

    def perform_destroy(self, instance):
        """Override to delete order item and update total amount"""
        order = instance.order
        instance.delete()

        # Update the order's total amount after deletion
        order.update_total_amount()
