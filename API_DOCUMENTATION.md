# Rural Mart API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [User Management API](#user-management-api)
4. [Products API](#products-api)
5. [Orders API](#orders-api)
6. [Payments API](#payments-api)
7. [Data Models](#data-models)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Examples](#examples)

## Overview

The Rural Mart API is a Django REST Framework-based e-commerce API that provides comprehensive functionality for managing users, products, orders, and payments. The API supports JWT authentication and follows RESTful conventions.

**Base URL**: `http://localhost:8000/`

**API Version**: v1

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. All authenticated endpoints require a valid access token in the Authorization header.

### Token Endpoints

#### Get Access Token
```http
POST /users/auth/api/token/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}
```

**Response:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Refresh Access Token
```http
POST /users/auth/api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
    "access": "new_access_token"
}
```

### Using Authentication
Include the access token in the Authorization header for all authenticated requests:
```http
Authorization: Bearer your_access_token
```

## User Management API

### User Registration
```http
POST /users/auth/register/
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone_number": "+254712345678",
    "roles": "buyer",
    "password": "secure_password"
}
```

**Response:**
```json
{
    "message": "The user registered successfully.",
    "user": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "+254712345678",
        "roles": "buyer"
    }
}
```

### User Login
```http
POST /users/auth/login/
Content-Type: application/json

{
    "email": "john.doe@example.com",
    "password": "secure_password"
}
```

**Response:**
```json
{
    "refresh": "refresh_token",
    "access": "access_token",
    "user": {
        "id": 1,
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "roles": "buyer"
    }
}
```

### User Logout
```http
POST /users/auth/logout/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
    "message": "User logged out successfully"
}
```

### Get User List (Admin Only)
```http
GET /users/auth/list/
Authorization: Bearer your_access_token
```

### Get User Details
```http
GET /users/auth/detail/{user_id}/
Authorization: Bearer your_access_token
```

### Update User
```http
PUT /users/auth/update/{user_id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "first_name": "Updated Name",
    "email": "updated@example.com"
}
```

### Delete User
```http
DELETE /users/auth/delete/{user_id}/
Authorization: Bearer your_access_token
```

### User Profile Management

#### Get User Profiles
```http
GET /users/auth/profiles/
Authorization: Bearer your_access_token
```

#### Get User Profile Details
```http
GET /users/auth/profiles/{profile_id}/
Authorization: Bearer your_access_token
```

#### Create User Profile
```http
POST /users/auth/profiles/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "address": "123 Main Street, Nairobi",
    "bio": "A brief bio about the user"
}
```

#### Update User Profile
```http
PUT /users/auth/profiles/{profile_id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "address": "Updated address",
    "bio": "Updated bio"
}
```

#### Delete User Profile
```http
DELETE /users/auth/profiles/{profile_id}/
Authorization: Bearer your_access_token
```

## Products API

### Products

#### Get All Products
```http
GET /api/products/
```

**Query Parameters:**
- `search`: Search in product name and description
- `category`: Filter by category ID
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `ordering`: Sort by field (price, name, created_at)
- `page`: Page number for pagination

**Example:**
```http
GET /api/products/?search=rice&min_price=100&max_price=500&ordering=price
```

#### Get Product Details
```http
GET /api/products/{product_id}/
```

#### Create Product (Admin/Vendor Only)
```http
POST /api/products/
Authorization: Bearer your_access_token
Content-Type: multipart/form-data

{
    "name": "Organic Rice",
    "description": "High-quality organic rice",
    "price": "250.00",
    "category": 1,
    "image": [file upload]
}
```

#### Update Product
```http
PUT /api/products/{product_id}/
Authorization: Bearer your_access_token
Content-Type: multipart/form-data
```

#### Delete Product
```http
DELETE /api/products/{product_id}/
Authorization: Bearer your_access_token
```

### Categories

#### Get All Categories
```http
GET /api/categories/
```

#### Get Category Details
```http
GET /api/categories/{category_id}/
```

#### Create Category
```http
POST /api/categories/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "name": "Grains",
    "parent_category": null
}
```

#### Update Category
```http
PUT /api/categories/{category_id}/
Authorization: Bearer your_access_token
```

#### Delete Category
```http
DELETE /api/categories/{category_id}/
Authorization: Bearer your_access_token
```

### Shopping Cart

#### Get User Cart
```http
GET /api/carts/
Authorization: Bearer your_access_token
```

#### Create Cart
```http
POST /api/carts/
Authorization: Bearer your_access_token
```

#### Update Cart
```http
PUT /api/carts/{cart_id}/
Authorization: Bearer your_access_token
```

#### Delete Cart
```http
DELETE /api/carts/{cart_id}/
Authorization: Bearer your_access_token
```

### Cart Items

#### Get Cart Items
```http
GET /api/cart-items/
Authorization: Bearer your_access_token
```

#### Add Item to Cart
```http
POST /api/cart-items/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "product": 1,
    "quantity": 2
}
```

#### Update Cart Item
```http
PUT /api/cart-items/{item_id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "quantity": 3
}
```

#### Remove Item from Cart
```http
DELETE /api/cart-items/{item_id}/
Authorization: Bearer your_access_token
```

## Orders API

### Orders

#### Get User Orders
```http
GET /api/orders/
Authorization: Bearer your_access_token
```

#### Get Order Details
```http
GET /api/orders/{order_id}/
Authorization: Bearer your_access_token
```

#### Create Order
```http
POST /api/orders/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "status": "pending"
}
```

#### Update Order Status
```http
PUT /api/orders/{order_id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "status": "processing"
}
```

#### Delete Order
```http
DELETE /api/orders/{order_id}/
Authorization: Bearer your_access_token
```

### Order Items

#### Get Order Items
```http
GET /api/orders/{order_id}/order-items/
Authorization: Bearer your_access_token
```

#### Add Item to Order
```http
POST /api/orders/{order_id}/order-items/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "product": 1,
    "quantity": 2,
    "unit_price": "250.00"
}
```

#### Update Order Item
```http
PUT /api/orders/{order_id}/order-items/{item_id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "quantity": 3,
    "unit_price": "250.00"
}
```

#### Remove Item from Order
```http
DELETE /api/orders/{order_id}/order-items/{item_id}/
Authorization: Bearer your_access_token
```

### Custom Order Actions

#### Add Item to Order (Custom Action)
```http
POST /api/orders/{order_id}/add_item/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "product": 1,
    "quantity": 2,
    "unit_price": "250.00"
}
```

#### Remove Item from Order (Custom Action)
```http
POST /api/orders/{order_id}/remove_item/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "item_id": 1
}
```

## Payments API

### Create Payment
```http
POST /api/create-payment/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "order_id": 1,
    "payment_method_id": 1
}
```

**Response:**
```json
{
    "id": 1,
    "user": 1,
    "order": 1,
    "amount": "500.00",
    "payment_method": {
        "id": 1,
        "name": "M-Pesa",
        "description": "Mobile money payment"
    },
    "status": "pending",
    "payment_date": "2024-01-15T10:30:00Z",
    "transaction_reference": null,
    "payment_gateway": null
}
```

### Process Payment
```http
POST /api/process-payment/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "payment_id": 1,
    "transaction_reference": "TXN123456789",
    "payment_gateway": "paystack",
    "amount": "500.00"
}
```

**Response:**
```json
{
    "transaction_id": "TXN123456789",
    "payment": {
        "id": 1,
        "user": 1,
        "order": 1,
        "amount": "500.00",
        "payment_method": {
            "id": 1,
            "name": "M-Pesa",
            "description": "Mobile money payment"
        },
        "status": "completed",
        "payment_date": "2024-01-15T10:30:00Z",
        "transaction_reference": "TXN123456789",
        "payment_gateway": "paystack"
    },
    "amount": "500.00",
    "status": "completed",
    "transaction_date": "2024-01-15T10:30:00Z",
    "payment_gateway_response": {
        "message": "Payment processed successfully"
    }
}
```

### Get Payment Status
```http
GET /api/payment-status/{payment_id}/
Authorization: Bearer your_access_token
```

## Data Models

### User Model
```python
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+254712345678",
    "roles": "buyer",  # Options: buyer, admin, vendor
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

### UserProfile Model
```python
{
    "id": 1,
    "user": 1,
    "address": "123 Main Street, Nairobi",
    "bio": "A brief bio about the user",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

### Category Model
```python
{
    "id": 1,
    "name": "Grains",
    "parent_category": null,  # For subcategories
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

### Product Model
```python
{
    "id": 1,
    "name": "Organic Rice",
    "description": "High-quality organic rice",
    "price": "250.00",
    "image": "/media/product_images/rice.jpg",
    "category": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

### Cart Model
```python
{
    "id": 1,
    "user": "john.doe@example.com",
    "total": "500.00",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

### CartItem Model
```python
{
    "id": 1,
    "cart": 1,
    "product": 1,
    "quantity": 2,
    "added_at": "2024-01-15T10:30:00Z"
}
```

### Order Model
```python
{
    "id": 1,
    "user": "john.doe@example.com",
    "order_date": "2024-01-15T10:30:00Z",
    "status": "pending",  # Options: pending, processing, shipped, delivered, cancelled
    "total_amount": "500.00",
    "order_items": [
        {
            "id": 1,
            "product": {
                "id": 1,
                "name": "Organic Rice",
                "description": "High-quality organic rice",
                "price": "250.00",
                "image": "/media/product_images/rice.jpg",
                "category": 1
            },
            "quantity": 2,
            "unit_price": "250.00",
            "total_price": "500.00"
        }
    ]
}
```

### Payment Model
```python
{
    "id": 1,
    "user": 1,
    "order": 1,
    "amount": "500.00",
    "payment_method": {
        "id": 1,
        "name": "M-Pesa",
        "description": "Mobile money payment"
    },
    "status": "completed",  # Options: pending, completed, failed, cancelled
    "payment_date": "2024-01-15T10:30:00Z",
    "transaction_reference": "TXN123456789",
    "payment_gateway": "paystack"
}
```

## Error Handling

The API returns standard HTTP status codes and error messages:

### Common Error Responses

#### 400 Bad Request
```json
{
    "detail": "Invalid data provided",
    "field_name": ["Specific error message"]
}
```

#### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

#### 404 Not Found
```json
{
    "detail": "Not found."
}
```

#### 500 Internal Server Error
```json
{
    "detail": "Internal server error occurred."
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Limits are applied per user and endpoint.

## Examples

### Complete Shopping Flow

#### 1. Register User
```bash
curl -X POST http://localhost:8000/users/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone_number": "+254712345678",
    "roles": "buyer",
    "password": "secure_password"
  }'
```

#### 2. Login
```bash
curl -X POST http://localhost:8000/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "secure_password"
  }'
```

#### 3. Browse Products
```bash
curl -X GET "http://localhost:8000/api/products/?search=rice&min_price=100&max_price=500" \
  -H "Authorization: Bearer your_access_token"
```

#### 4. Add to Cart
```bash
curl -X POST http://localhost:8000/api/cart-items/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "quantity": 2
  }'
```

#### 5. Create Order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "pending"
  }'
```

#### 6. Add Items to Order
```bash
curl -X POST http://localhost:8000/api/orders/1/order-items/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "quantity": 2,
    "unit_price": "250.00"
  }'
```

#### 7. Create Payment
```bash
curl -X POST http://localhost:8000/api/create-payment/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "payment_method_id": 1
  }'
```

#### 8. Process Payment
```bash
curl -X POST http://localhost:8000/api/process-payment/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_id": 1,
    "transaction_reference": "TXN123456789",
    "payment_gateway": "paystack",
    "amount": "500.00"
  }'
```

### Python Client Example

```python
import requests
import json

class RuralMartAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
        
    def login(self, email, password):
        response = requests.post(
            f"{self.base_url}/users/auth/login/",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access"]
            return data
        else:
            raise Exception("Login failed")
    
    def get_products(self, **filters):
        headers = {"Authorization": f"Bearer {self.access_token}"} if self.access_token else {}
        params = {k: v for k, v in filters.items() if v is not None}
        response = requests.get(f"{self.base_url}/api/products/", headers=headers, params=params)
        return response.json()
    
    def add_to_cart(self, product_id, quantity):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(
            f"{self.base_url}/api/cart-items/",
            headers=headers,
            json={"product": product_id, "quantity": quantity}
        )
        return response.json()
    
    def create_order(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(
            f"{self.base_url}/api/orders/",
            headers=headers,
            json={"status": "pending"}
        )
        return response.json()

# Usage
api = RuralMartAPI()
api.login("john.doe@example.com", "secure_password")
products = api.get_products(search="rice", min_price=100)
api.add_to_cart(product_id=1, quantity=2)
order = api.create_order()
```

### JavaScript/Node.js Client Example

```javascript
class RuralMartAPI {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
        this.accessToken = null;
    }
    
    async login(email, password) {
        const response = await fetch(`${this.baseUrl}/users/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            this.accessToken = data.access;
            return data;
        } else {
            throw new Error('Login failed');
        }
    }
    
    async getProducts(filters = {}) {
        const headers = this.accessToken ? 
            { 'Authorization': `Bearer ${this.accessToken}` } : {};
        
        const params = new URLSearchParams(filters);
        const response = await fetch(
            `${this.baseUrl}/api/products/?${params}`,
            { headers }
        );
        
        return response.json();
    }
    
    async addToCart(productId, quantity) {
        const response = await fetch(`${this.baseUrl}/api/cart-items/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.accessToken}`
            },
            body: JSON.stringify({ product: productId, quantity })
        });
        
        return response.json();
    }
    
    async createOrder() {
        const response = await fetch(`${this.baseUrl}/api/orders/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.accessToken}`
            },
            body: JSON.stringify({ status: 'pending' })
        });
        
        return response.json();
    }
}

// Usage
const api = new RuralMartAPI();
api.login('john.doe@example.com', 'secure_password')
    .then(() => api.getProducts({ search: 'rice', min_price: 100 }))
    .then(products => console.log(products))
    .then(() => api.addToCart(1, 2))
    .then(() => api.createOrder())
    .catch(error => console.error(error));
```

## Additional Notes

- All timestamps are in ISO 8601 format (UTC)
- File uploads for product images use multipart/form-data
- The API supports pagination for list endpoints
- Filtering and searching are available on most list endpoints
- All monetary values are in decimal format with 2 decimal places
- The API follows RESTful conventions and uses standard HTTP methods
- JWT tokens have expiration times that can be configured in settings
- The API includes comprehensive error handling and validation