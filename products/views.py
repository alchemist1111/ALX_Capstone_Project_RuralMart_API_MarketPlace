from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Category, Cart, CartItem
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend

# Product viewset
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    # Filter backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Custom filterset
    filterset_class = ProductFilter
    
    # Search set up
    search_fields = ['name', 'description']
    
    # Ordering set up
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['name']
    
    
    
# Category viewset
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    
# Cart viewset
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Each user can only see their own carts
        return Cart.objects.filter(user=self.request.user) 
    
    def perform_create(self, serializer):
        # Automatically assign cart to the logged-in user
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):    
        # Prevent users from updating someone else's cart
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You cannot modify another user's cart.")
        serializer.save()
        
    def perform_destroy(self, instance):
        # Prevent users from deleting someone else's cart
        if instance.user != self.request.user:
            raise PermissionDenied("You cannot delete another user's cart.")
        instance.delete()    
    
         


# Cart item viewset
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see items in their own carts
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the cart item to the user's cart
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

    def perform_update(self, serializer):
        # Ensure the user can only update their own cart items
        if serializer.instance.cart.user != self.request.user:
            raise PermissionDenied("You cannot modify items in another user's cart.")
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure the user can only delete their own cart items
        if instance.cart.user != self.request.user:
            raise PermissionDenied("You cannot delete items from another user's cart.")
        instance.delete()  
    
    
