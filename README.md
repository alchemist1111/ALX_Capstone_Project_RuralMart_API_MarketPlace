# Rural Mart API

A comprehensive Django REST Framework-based e-commerce API for rural market management, featuring user authentication, product management, order processing, and payment integration.

## 🚀 Features

- **User Management**: Registration, authentication, and profile management with role-based access control
- **Product Catalog**: Product and category management with advanced filtering and search
- **Shopping Cart**: Add, update, and remove items from shopping cart
- **Order Management**: Complete order lifecycle from creation to delivery
- **Payment Integration**: Paystack payment gateway integration
- **JWT Authentication**: Secure token-based authentication
- **RESTful API**: Standard REST conventions with comprehensive endpoints
- **Admin Interface**: Django admin for backend management

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🏃‍♂️ Quick Start

### Prerequisites

- Python 3.8+
- Django 4.0+
- PostgreSQL (recommended) or SQLite
- Redis (for caching, optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rural-mart-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

### Main Documentation
- **[Complete API Documentation](API_DOCUMENTATION.md)** - Comprehensive guide to all endpoints, models, and usage examples
- **[Utility Functions Documentation](UTILITY_FUNCTIONS_DOCUMENTATION.md)** - Detailed documentation of helper functions and components

### Quick API Reference

#### Authentication Endpoints
- `POST /users/auth/register/` - User registration
- `POST /users/auth/login/` - User login
- `POST /users/auth/logout/` - User logout
- `POST /users/auth/api/token/` - Get JWT tokens
- `POST /users/auth/api/token/refresh/` - Refresh JWT tokens

#### Product Endpoints
- `GET /api/products/` - List products (with filtering)
- `POST /api/products/` - Create product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

#### Order Endpoints
- `GET /api/orders/` - List user orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Get order details
- `PUT /api/orders/{id}/` - Update order status

#### Payment Endpoints
- `POST /api/create-payment/` - Create payment
- `POST /api/process-payment/` - Process payment
- `GET /api/payment-status/{id}/` - Get payment status

## 🏗️ Project Structure

```
rural_mart/
├── accounts/                 # User management app
│   ├── models.py            # User and UserProfile models
│   ├── views.py             # Authentication and user views
│   ├── serializers.py       # User serializers
│   ├── tokens.py            # JWT token utilities
│   ├── permissions.py       # Custom permissions
│   └── signals.py           # User profile signals
├── products/                # Product management app
│   ├── models.py            # Product, Category, Cart models
│   ├── views.py             # Product and cart views
│   ├── serializers.py       # Product serializers
│   ├── filters.py           # Product filtering
│   └── cart_utils.py        # Cart calculation utilities
├── orders/                  # Order management app
│   ├── models.py            # Order and OrderItem models
│   ├── views.py             # Order views
│   └── serializers.py       # Order serializers
├── payments/                # Payment processing app
│   ├── models.py            # Payment and Transaction models
│   ├── views.py             # Payment views
│   ├── serializers.py       # Payment serializers
│   └── paystack_service.py  # Paystack integration
├── rural_mart/              # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
├── API_DOCUMENTATION.md     # Complete API documentation
├── UTILITY_FUNCTIONS_DOCUMENTATION.md  # Utility functions guide
└── README.md               # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/rural_mart

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Paystack Settings
PAYSTACK_SECRET_KEY=your-paystack-secret-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Django Settings

Key settings in `rural_mart/settings.py`:

```python
# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## 💡 Usage Examples

### Basic API Usage

#### 1. User Registration and Login

```python
import requests

# Register a new user
response = requests.post('http://localhost:8000/users/auth/register/', json={
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john.doe@example.com',
    'phone_number': '+254712345678',
    'roles': 'buyer',
    'password': 'secure_password'
})

# Login to get tokens
response = requests.post('http://localhost:8000/users/auth/login/', json={
    'email': 'john.doe@example.com',
    'password': 'secure_password'
})

tokens = response.json()
access_token = tokens['access']
```

#### 2. Browse Products

```python
# Get all products
response = requests.get('http://localhost:8000/api/products/')
products = response.json()

# Search and filter products
response = requests.get('http://localhost:8000/api/products/', params={
    'search': 'rice',
    'min_price': 100,
    'max_price': 500,
    'category': 1,
    'ordering': 'price'
})
filtered_products = response.json()
```

#### 3. Shopping Cart Operations

```python
headers = {'Authorization': f'Bearer {access_token}'}

# Add item to cart
response = requests.post('http://localhost:8000/api/cart-items/', 
    headers=headers,
    json={'product': 1, 'quantity': 2}
)

# Get cart items
response = requests.get('http://localhost:8000/api/cart-items/', headers=headers)
cart_items = response.json()
```

#### 4. Create and Process Order

```python
# Create order
response = requests.post('http://localhost:8000/api/orders/',
    headers=headers,
    json={'status': 'pending'}
)
order = response.json()

# Add items to order
response = requests.post(f'http://localhost:8000/api/orders/{order["id"]}/order-items/',
    headers=headers,
    json={
        'product': 1,
        'quantity': 2,
        'unit_price': '250.00'
    }
)

# Create payment
response = requests.post('http://localhost:8000/api/create-payment/',
    headers=headers,
    json={
        'order_id': order['id'],
        'payment_method_id': 1
    }
)
payment = response.json()
```

### Complete Shopping Flow Example

See the [API Documentation](API_DOCUMENTATION.md#complete-shopping-flow) for a complete example of the entire shopping process from registration to payment.

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test products
python manage.py test orders
python manage.py test payments

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Data

The project includes utility functions for creating test data:

```python
from accounts.models import User
from products.models import Category, Product

# Create test user
user = User.objects.create_user(
    email='test@example.com',
    password='testpass123',
    first_name='Test',
    last_name='User'
)

# Create test category
category = Category.objects.create(name='Test Category')

# Create test product
product = Product.objects.create(
    name='Test Product',
    description='Test description',
    price='100.00',
    category=category
)
```

## 🚀 Deployment

### Production Setup

1. **Set up production database**
   ```bash
   # PostgreSQL recommended for production
   createdb rural_mart_prod
   ```

2. **Configure environment variables**
   ```bash
   # Set DEBUG=False and configure production settings
   export DEBUG=False
   export SECRET_KEY=your-production-secret-key
   ```

3. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Set up web server**
   - Use Gunicorn with Nginx
   - Configure SSL certificates
   - Set up proper firewall rules

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "rural_mart.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for any API changes
- Use meaningful commit messages
- Add type hints where appropriate

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [API Documentation](API_DOCUMENTATION.md)
- **Issues**: Create an issue on GitHub
- **Email**: support@ruralmart.com

## 🔗 Related Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Paystack API Documentation](https://paystack.com/docs/)

---

**Rural Mart API** - Empowering rural commerce through technology.