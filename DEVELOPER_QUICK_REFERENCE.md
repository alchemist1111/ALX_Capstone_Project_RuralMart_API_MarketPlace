# Rural Mart API - Developer Quick Reference

## 🚀 Quick Start Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Testing
python manage.py test
python manage.py test accounts
python manage.py test products

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py shell

# Admin
python manage.py createsuperuser
python manage.py collectstatic
```

## 📋 API Endpoints Quick Reference

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/users/auth/register/` | User registration | No |
| POST | `/users/auth/login/` | User login | No |
| POST | `/users/auth/logout/` | User logout | Yes |
| POST | `/users/auth/api/token/` | Get JWT tokens | No |
| POST | `/users/auth/api/token/refresh/` | Refresh JWT tokens | No |

### Users
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/auth/list/` | List users | Yes (Admin) |
| GET | `/users/auth/detail/{id}/` | Get user details | Yes |
| PUT | `/users/auth/update/{id}/` | Update user | Yes |
| DELETE | `/users/auth/delete/{id}/` | Delete user | Yes |

### User Profiles
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/auth/profiles/` | List profiles | Yes |
| GET | `/users/auth/profiles/{id}/` | Get profile | Yes |
| POST | `/users/auth/profiles/` | Create profile | Yes |
| PUT | `/users/auth/profiles/{id}/` | Update profile | Yes |
| DELETE | `/users/auth/profiles/{id}/` | Delete profile | Yes |

### Products
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/` | List products | No |
| POST | `/api/products/` | Create product | Yes |
| GET | `/api/products/{id}/` | Get product | No |
| PUT | `/api/products/{id}/` | Update product | Yes |
| DELETE | `/api/products/{id}/` | Delete product | Yes |

### Categories
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | List categories | No |
| POST | `/api/categories/` | Create category | Yes |
| GET | `/api/categories/{id}/` | Get category | No |
| PUT | `/api/categories/{id}/` | Update category | Yes |
| DELETE | `/api/categories/{id}/` | Delete category | Yes |

### Cart
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/carts/` | Get user cart | Yes |
| POST | `/api/carts/` | Create cart | Yes |
| PUT | `/api/carts/{id}/` | Update cart | Yes |
| DELETE | `/api/carts/{id}/` | Delete cart | Yes |

### Cart Items
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/cart-items/` | List cart items | Yes |
| POST | `/api/cart-items/` | Add to cart | Yes |
| PUT | `/api/cart-items/{id}/` | Update cart item | Yes |
| DELETE | `/api/cart-items/{id}/` | Remove from cart | Yes |

### Orders
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/` | List user orders | Yes |
| POST | `/api/orders/` | Create order | Yes |
| GET | `/api/orders/{id}/` | Get order | Yes |
| PUT | `/api/orders/{id}/` | Update order | Yes |
| DELETE | `/api/orders/{id}/` | Delete order | Yes |
| POST | `/api/orders/{id}/add_item/` | Add item to order | Yes |
| POST | `/api/orders/{id}/remove_item/` | Remove item from order | Yes |

### Order Items
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/{order_id}/order-items/` | List order items | Yes |
| POST | `/api/orders/{order_id}/order-items/` | Add order item | Yes |
| PUT | `/api/orders/{order_id}/order-items/{id}/` | Update order item | Yes |
| DELETE | `/api/orders/{order_id}/order-items/{id}/` | Remove order item | Yes |

### Payments
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/create-payment/` | Create payment | Yes |
| POST | `/api/process-payment/` | Process payment | Yes |
| GET | `/api/payment-status/{id}/` | Get payment status | Yes |

## 🔧 Common Code Patterns

### Authentication Headers
```python
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
```

### API Client Setup
```python
import requests

class RuralMartClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
    
    def login(self, email, password):
        response = requests.post(f"{self.base_url}/users/auth/login/", json={
            'email': email,
            'password': password
        })
        data = response.json()
        self.access_token = data['access']
        return data
```

### Error Handling
```python
try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    print(f"API Error: {e}")
    return None
```

## 📊 Data Models Quick Reference

### User Model
```python
{
    'id': 1,
    'email': 'user@example.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'phone_number': '+254712345678',
    'roles': 'buyer',  # buyer, admin, vendor
    'created_at': '2024-01-15T10:30:00Z',
    'updated_at': '2024-01-15T10:30:00Z'
}
```

### Product Model
```python
{
    'id': 1,
    'name': 'Organic Rice',
    'description': 'High-quality organic rice',
    'price': '250.00',
    'image': '/media/product_images/rice.jpg',
    'category': 1,
    'created_at': '2024-01-15T10:30:00Z',
    'updated_at': '2024-01-15T10:30:00Z'
}
```

### Order Model
```python
{
    'id': 1,
    'user': 'john.doe@example.com',
    'order_date': '2024-01-15T10:30:00Z',
    'status': 'pending',  # pending, processing, shipped, delivered, cancelled
    'total_amount': '500.00',
    'order_items': [...]
}
```

### Payment Model
```python
{
    'id': 1,
    'user': 1,
    'order': 1,
    'amount': '500.00',
    'payment_method': {...},
    'status': 'completed',  # pending, completed, failed, cancelled
    'payment_date': '2024-01-15T10:30:00Z',
    'transaction_reference': 'TXN123456789',
    'payment_gateway': 'paystack'
}
```

## 🔍 Query Parameters

### Product Filtering
```python
# Search and filter products
params = {
    'search': 'rice',           # Search in name/description
    'category': 1,              # Filter by category
    'min_price': 100,           # Minimum price
    'max_price': 500,           # Maximum price
    'ordering': 'price',        # Sort by: price, name, created_at
    'page': 1                   # Pagination
}

response = requests.get('/api/products/', params=params)
```

### Pagination
```python
# Default pagination response
{
    'count': 100,
    'next': 'http://localhost:8000/api/products/?page=2',
    'previous': None,
    'results': [...]
}
```

## 🛠️ Utility Functions

### Token Management
```python
from accounts.tokens import generate_tokens, blacklist_token

# Generate tokens
tokens = generate_tokens(user)

# Blacklist token
success = blacklist_token(refresh_token)
```

### Cart Calculations
```python
from products.cart_utils import calculate_cart_total, calculate_cart_item_total

# Calculate cart total
total = calculate_cart_total(cart)

# Calculate item total
item_total = calculate_cart_item_total(cart_item)
```

### Product Filtering
```python
from products.filters import ProductFilter

# Create filter instance
filter_set = ProductFilter(data={
    'min_price': 100,
    'max_price': 500,
    'category': 1,
    'search': 'rice'
})

# Apply filters
filtered_products = filter_set.qs
```

## 🔐 Permissions

### Permission Classes
```python
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.permissions import IsAdminUser

# Public endpoint
permission_classes = [AllowAny]

# Authenticated users only
permission_classes = [IsAuthenticated]

# Admin users only
permission_classes = [IsAdminUser]
```

### Custom Permission Check
```python
def get_object(self):
    obj = super().get_object()
    if obj.user != self.request.user:
        raise PermissionDenied("You can only access your own data.")
    return obj
```

## 🧪 Testing Patterns

### Test User Creation
```python
from accounts.models import User

def create_test_user(email="test@example.com", role="buyer"):
    return User.objects.create_user(
        email=email,
        password="testpass123",
        first_name="Test",
        last_name="User",
        phone_number="+254712345678",
        roles=role
    )
```

### API Test Client
```python
from rest_framework.test import APIClient

client = APIClient()
client.force_authenticate(user=user)

# Make authenticated request
response = client.get('/api/orders/')
```

### Test Data Setup
```python
from products.models import Category, Product

def setUp(self):
    self.user = create_test_user()
    self.category = Category.objects.create(name="Test Category")
    self.product = Product.objects.create(
        name="Test Product",
        description="Test description",
        price="100.00",
        category=self.category
    )
```

## 🚀 Deployment Checklist

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@localhost:5432/rural_mart
PAYSTACK_SECRET_KEY=your-paystack-secret-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
```

### Production Commands
```bash
python manage.py collectstatic
python manage.py migrate
python manage.py check --deploy
```

### Security Checklist
- [ ] DEBUG=False
- [ ] Strong SECRET_KEY
- [ ] HTTPS enabled
- [ ] Database backups configured
- [ ] Rate limiting enabled
- [ ] CORS configured
- [ ] Static files served by web server

## 📝 Common Issues & Solutions

### JWT Token Issues
```python
# Token expired
if response.status_code == 401:
    # Refresh token
    refresh_response = requests.post('/users/auth/api/token/refresh/', json={
        'refresh': refresh_token
    })
    new_access_token = refresh_response.json()['access']
```

### File Upload Issues
```python
# For product images
files = {'image': open('product.jpg', 'rb')}
data = {
    'name': 'Product Name',
    'description': 'Description',
    'price': '100.00',
    'category': 1
}
response = requests.post('/api/products/', data=data, files=files)
```

### Database Connection Issues
```python
# Check database connection
python manage.py dbshell

# Reset migrations (development only)
python manage.py migrate --fake-initial
```

## 🔗 Useful Links

- [API Documentation](API_DOCUMENTATION.md)
- [Utility Functions Documentation](UTILITY_FUNCTIONS_DOCUMENTATION.md)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Paystack API](https://paystack.com/docs/)

---

**Quick Reference** - Keep this handy for daily development!