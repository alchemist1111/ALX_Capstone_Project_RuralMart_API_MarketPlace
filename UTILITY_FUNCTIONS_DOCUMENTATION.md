# Rural Mart API - Utility Functions & Components Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication Utilities](#authentication-utilities)
3. [Cart Utilities](#cart-utilities)
4. [Product Filters](#product-filters)
5. [Payment Services](#payment-services)
6. [Permissions](#permissions)
7. [Signals](#signals)
8. [Admin Interfaces](#admin-interfaces)

## Overview

This document provides detailed documentation for utility functions, helper classes, and components used throughout the Rural Mart API. These utilities provide essential functionality for authentication, cart management, filtering, payments, and more.

## Authentication Utilities

### Token Management (`accounts/tokens.py`)

#### `generate_tokens(user)`
Generates JWT access and refresh tokens for a user.

**Parameters:**
- `user`: User instance to generate tokens for

**Returns:**
```python
{
    'refresh': 'refresh_token_string',
    'access': 'access_token_string'
}
```

**Usage:**
```python
from accounts.tokens import generate_tokens

# Generate tokens for a user
tokens = generate_tokens(user)
access_token = tokens['access']
refresh_token = tokens['refresh']
```

#### `blacklist_token(refresh_token)`
Blacklists a refresh token to prevent its future use.

**Parameters:**
- `refresh_token`: The refresh token string to blacklist

**Returns:**
- `True`: If token was successfully blacklisted
- `False`: If there was an error blacklisting the token

**Usage:**
```python
from accounts.tokens import blacklist_token

# Blacklist a refresh token during logout
success = blacklist_token(refresh_token)
if success:
    print("Token blacklisted successfully")
else:
    print("Error blacklisting token")
```

## Cart Utilities (`products/cart_utils.py`)

### `calculate_cart_total(cart)`
Calculates the total price of all items in a shopping cart.

**Parameters:**
- `cart`: Cart instance to calculate total for

**Returns:**
- `Decimal`: Total price of all items in the cart

**Usage:**
```python
from products.cart_utils import calculate_cart_total

# Calculate total for a user's cart
cart = Cart.objects.get(user=user)
total = calculate_cart_total(cart)
print(f"Cart total: ${total}")
```

### `calculate_cart_item_total(cart_item)`
Calculates the total price for a specific cart item (product price × quantity).

**Parameters:**
- `cart_item`: CartItem instance to calculate total for

**Returns:**
- `Decimal`: Total price for the cart item

**Usage:**
```python
from products.cart_utils import calculate_cart_item_total

# Calculate total for a specific cart item
cart_item = CartItem.objects.get(id=1)
item_total = calculate_cart_item_total(cart_item)
print(f"Item total: ${item_total}")
```

## Product Filters (`products/filters.py`)

### `ProductFilter`
A Django FilterSet class that provides advanced filtering capabilities for products.

**Available Filters:**

#### Price Range Filters
- `min_price`: Filter products with price greater than or equal to specified value
- `max_price`: Filter products with price less than or equal to specified value

#### Category Filter
- `category`: Filter products by category ID

#### Search Filter
- `search`: Search in product name using case-insensitive contains lookup

#### Ordering Filter
- `ordering`: Sort products by price, created_at, or name

**Usage:**
```python
from products.filters import ProductFilter

# Create filter instance
filter_set = ProductFilter(data={
    'min_price': 100,
    'max_price': 500,
    'category': 1,
    'search': 'rice',
    'ordering': 'price'
})

# Apply filters to queryset
filtered_products = filter_set.qs
```

**Example API Requests:**
```http
GET /api/products/?min_price=100&max_price=500&category=1&search=rice&ordering=price
```

## Payment Services (`payments/paystack_service.py`)

### Paystack Integration

#### `verify_payment(transaction_reference)`
Verifies a payment transaction with Paystack.

**Parameters:**
- `transaction_reference`: The transaction reference from Paystack

**Returns:**
- `dict`: Paystack verification response or error message

**Usage:**
```python
from payments.paystack_service import verify_payment

# Verify a payment
result = verify_payment("TXN123456789")
if "error" not in result:
    print("Payment verified successfully")
    print(f"Status: {result['status']}")
else:
    print(f"Verification failed: {result['error']}")
```

#### `initialize_payment(email, amount, order_id)`
Initializes a new payment with Paystack.

**Parameters:**
- `email`: Customer's email address
- `amount`: Payment amount (will be multiplied by 100 for Paystack)
- `order_id`: Order ID for reference

**Returns:**
- `dict`: Paystack initialization response or error message

**Usage:**
```python
from payments.paystack_service import initialize_payment

# Initialize a payment
result = initialize_payment(
    email="customer@example.com",
    amount=500.00,
    order_id="ORDER123"
)
if "error" not in result:
    print("Payment initialized")
    print(f"Reference: {result['reference']}")
else:
    print(f"Initialization failed: {result['error']}")
```

## Permissions (`accounts/permissions.py`)

### `IsAdminUser`
Custom permission class that checks if the user has admin role.

**Usage:**
```python
from accounts.permissions import IsAdminUser

class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Only admin users can access this view
        pass
```

**Implementation:**
```python
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.roles == 'admin'
```

## Signals (`accounts/signals.py`)

### User Profile Signal
Automatically creates a user profile when a new user is created.

**Signal:**
- `post_save` signal on User model

**Handler:**
```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

**Usage:**
The signal is automatically triggered when a new user is created. No manual intervention required.

**Example:**
```python
# When a user is created, a profile is automatically created
user = User.objects.create_user(
    email="newuser@example.com",
    password="password123",
    first_name="John",
    last_name="Doe"
)

# UserProfile is automatically created
profile = user.userprofile
print(f"Profile created: {profile}")
```

## Admin Interfaces

### User Admin (`accounts/admin.py`)
Provides Django admin interface for User model management.

**Features:**
- User list with search and filtering
- User creation and editing
- Role management
- Password management

### Product Admin (`products/admin.py`)
Provides Django admin interface for Product and Category models.

**Features:**
- Product management with image upload
- Category management with hierarchical structure
- Cart and cart item management
- Search and filtering capabilities

### Order Admin (`orders/admin.py`)
Provides Django admin interface for Order and OrderItem models.

**Features:**
- Order management with status tracking
- Order item management
- Total amount calculation
- User order filtering

### Payment Admin (`payments/admin.py`)
Provides Django admin interface for Payment and Transaction models.

**Features:**
- Payment tracking and management
- Transaction history
- Payment method management
- Status monitoring

## Model Methods

### User Model Methods

#### `__str__(self)`
Returns a string representation of the user.

**Returns:**
- `str`: "Name: {first_name} {last_name}, Email: {email}"

### Order Model Methods

#### `update_total_amount(self)`
Updates the total amount of the order based on related OrderItems.

**Usage:**
```python
order = Order.objects.get(id=1)
order.update_total_amount()
print(f"Updated total: ${order.total_amount}")
```

#### `save(self, *args, **kwargs)`
Overridden save method that automatically updates total amount.

### OrderItem Model Methods

#### `save(self, *args, **kwargs)`
Overridden save method that calculates total_price and updates order total.

### Payment Model Methods

#### `is_successful(self)`
Checks if the payment was successful.

**Returns:**
- `bool`: True if payment status is 'completed', False otherwise

**Usage:**
```python
payment = Payment.objects.get(id=1)
if payment.is_successful():
    print("Payment completed successfully")
else:
    print("Payment not completed")
```

## Serializer Methods

### UserRegistrationSerializer

#### `validate(self, data)`
Validates password confirmation and password strength.

**Parameters:**
- `data`: Serializer data dictionary

**Returns:**
- `dict`: Validated data

**Raises:**
- `ValidationError`: If passwords don't match or password is invalid

#### `create(self, validated_data)`
Creates a new user with hashed password.

**Parameters:**
- `validated_data`: Validated serializer data

**Returns:**
- `User`: Created user instance

### OrderSerializer

#### `create(self, validated_data)`
Creates an order with nested order items.

**Parameters:**
- `validated_data`: Validated serializer data

**Returns:**
- `Order`: Created order instance

#### `update(self, instance, validated_data)`
Updates an order and its items.

**Parameters:**
- `instance`: Order instance to update
- `validated_data`: Validated serializer data

**Returns:**
- `Order`: Updated order instance

## Error Handling

### Custom Exceptions

The API includes custom exception handling for various scenarios:

#### Validation Errors
```python
from rest_framework.exceptions import ValidationError

# Raise validation error
raise ValidationError("Invalid data provided")
```

#### Permission Denied
```python
from django.core.exceptions import PermissionDenied

# Raise permission error
raise PermissionDenied("You do not have permission to perform this action")
```

### Error Response Format
All errors follow a consistent format:
```json
{
    "detail": "Error message",
    "field_name": ["Specific field error"]
}
```

## Configuration

### JWT Settings
JWT token configuration is handled in Django settings:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### Paystack Configuration
Paystack integration requires API key configuration:

```python
PAYSTACK_SECRET_KEY = 'your_paystack_secret_key'
PAYSTACK_PUBLIC_KEY = 'your_paystack_public_key'
```

## Testing Utilities

### Test Data Creation
Utility functions for creating test data:

```python
def create_test_user(email="test@example.com", role="buyer"):
    """Create a test user for testing purposes."""
    return User.objects.create_user(
        email=email,
        password="testpass123",
        first_name="Test",
        last_name="User",
        phone_number="+254712345678",
        roles=role
    )

def create_test_product(name="Test Product", price="100.00"):
    """Create a test product for testing purposes."""
    category = Category.objects.create(name="Test Category")
    return Product.objects.create(
        name=name,
        description="Test product description",
        price=price,
        category=category
    )
```

## Performance Considerations

### Database Optimization
- Use `select_related()` and `prefetch_related()` for related field queries
- Implement database indexing on frequently queried fields
- Use pagination for large result sets

### Caching
Consider implementing caching for:
- Product listings
- Category hierarchies
- User profile data

### Query Optimization
```python
# Optimized product query with related data
products = Product.objects.select_related('category').prefetch_related('cartitem_set')

# Optimized order query with items
orders = Order.objects.select_related('user').prefetch_related('order_items__product')
```

## Security Considerations

### Password Security
- Passwords are hashed using Django's built-in password hashing
- Password validation is enforced during registration
- Password confirmation is required

### Token Security
- JWT tokens have configurable expiration times
- Refresh tokens can be blacklisted
- Access tokens are short-lived for security

### Data Validation
- All input data is validated through serializers
- File uploads are restricted to specific formats
- SQL injection is prevented through Django ORM

## Best Practices

### Code Organization
- Keep utility functions in dedicated modules
- Use meaningful function and variable names
- Add comprehensive docstrings for all functions

### Error Handling
- Always handle exceptions gracefully
- Provide meaningful error messages
- Log errors for debugging

### Testing
- Write unit tests for all utility functions
- Test edge cases and error conditions
- Use mock objects for external service calls

### Documentation
- Keep documentation up to date
- Include usage examples
- Document all parameters and return values