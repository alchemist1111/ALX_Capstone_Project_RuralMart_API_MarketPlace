````markdown
# ALX-Capstone-Project-RuralMart-API-MarketPlace

This is the backend API for the **RuralMart Marketplace**, built as part of the ALX Capstone project. The API provides endpoints to manage users, products, orders, payments, reviews, and other functionalities for a marketplace system aimed at rural communities.

## Table of Contents
- [Project Description](#project-description)
- [Tech Stack](#tech-stack)
- [Installation Guide](#installation-guide)
- [API Documentation](#api-documentation)
- [Key Features](#key-features)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Tests](#tests)
- [Contributing](#contributing)
- [License](#license)

## Project Description
**RuralMart Marketplace** is an e-commerce platform designed to connect rural sellers and buyers. The project is built using Django and Django REST Framework, providing a robust API to manage the operations of the marketplace.

### Key Features:
- **User Authentication & Authorization**: User registration, login, JWT authentication.
- **Product Management**: CRUD operations for products.
- **Order Management**: Buyers can place orders, and sellers can manage them.
- **Payment Integration**: Integration with payment systems for transaction processing.
- **Review Management**: Buyers can leave reviews for products.
- **Swagger Documentation**: Automatically generated API documentation using Swagger UI for easy exploration and testing of API endpoints.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: MySQL
- **Authentication**: JSON Web Tokens (JWT)
- **API Documentation**: Swagger UI (drf-yasg)
- **Deployment**: Database on AWS RDS and Backend on Render Cloud Application

## Installation Guide
Follow these steps to get the project up and running locally.

### Prerequisites
- Python 3.x
- MySQL (or any other supported database)
- Virtualenv (optional but recommended)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ALX-Capstone-Project-RuralMart-API-MarketPlace.git
cd ALX-Capstone-Project-RuralMart-API-MarketPlace
````

### 2. Set up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the Database

# Create a MySQL database

```bash
createdb ruralmart_db
```

# Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Start the server

```bash
python manage.py runserver
```

* Your API should now be accessible at [http://localhost:8000/](http://localhost:8000/).

## API Documentation

You can explore and interact with the API using the Swagger UI:

Swagger UI Documentation: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

## Authentication

To interact with authenticated endpoints, use JWT tokens.

* Login: Post your credentials to /users/auth/login/ to receive a JWT token.
* Authorization: Add the token as Authorization: Bearer \<your\_token> in the header when making requests to protected endpoints.

### Key Features:

1. **User Authentication and Authorization**

   * **User Registration**: New users can register an account by providing necessary details (such as name, email, and password).
   * **User Login**: Users can log in to the system by providing their credentials and receive a JWT token for authentication.
   * **JWT Authentication**: The API uses JSON Web Tokens (JWT) for secure authentication across endpoints. Each user has a unique token that needs to be included in request headers for access to protected routes.
   * **Role-Based Access**: Different roles (e.g., admin, seller, buyer) are implemented to control access to certain API resources.

2. **Product Management**

   * **Create Products**: Sellers can add new products to the marketplace by providing necessary information (e.g., name, description, price, category, etc.).
   * **Read Product Details**: Users can view product details through the API or via the Swagger UI.
   * **Update Products**: Sellers can update the details of their own products, including price, description, and availability.
   * **Delete Products**: Sellers can delete their own products from the marketplace.
   * **Product Categories**: Products are categorized, making it easier for buyers to search for products by category.

3. **Order Management**

   * **Create Orders**: Buyers can place orders by selecting products and proceeding to checkout.
   * **View Orders**: Users can view their own orders, including the order status (pending, shipped, delivered).
   * **Order Cancellation**: Buyers can cancel orders before they are shipped.
   * **Seller Order Management**: Sellers can view the orders placed for their products and mark them as shipped or delivered.
   * **Order History**: Users can view their past orders along with the status and details of each transaction.

4. **Payment Integration**

   * **Payment Processing**: Integration with a payment gateway allows users to make payments for orders.
   * **Secure Transactions**: Payments are processed securely, with payment data handled using industry-standard encryption protocols.
   * **Order Confirmation**: Once the payment is successful, the order is confirmed and marked as "paid."
   * **Transaction History**: Users can view the transaction history for their purchases.

5. **Review Management**

   * **Product Reviews**: Buyers can leave reviews for products they have purchased, helping other users make informed decisions.
   * **Review Ratings**: Reviews can include a rating (e.g., 1 to 5 stars) as well as a written comment.
   * **Moderation**: Reviews may be moderated by admins to ensure compliance with platform guidelines.
   * **View Reviews**: Users can view reviews left by others for products they are interested in.

6. **Swagger Documentation**

   * **Interactive API Docs**: The project includes automatically generated API documentation powered by Swagger UI, allowing developers to easily explore and test available API endpoints.
   * **API Testing**: With Swagger, users can test API endpoints directly from the documentation interface by making requests and seeing responses in real-time.
   * **Authentication Integration**: Swagger UI allows users to log in with a JWT token and access protected routes directly from the documentation.
   * **Comprehensive Endpoints**: The Swagger UI provides detailed descriptions of all available API endpoints, including required parameters and expected responses.

## Environment Variables

The project relies on environment variables for configuration, such as database settings, secret keys, etc.

Example:

```bash
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@localhost:5432/ruralmart_db
JWT_SECRET_KEY=your-jwt-secret-key
```

Make sure to create the .env file in the root of the project or set the environment variables manually.

## Usage

### Available API Endpoints

Here’s a quick overview of the available endpoints:

* **POST** `/users/auth/register/` - Register a new user
* **POST** `/users/auth/login/` - Login and obtain a JWT token
* **GET** `/api/products/` - List all products
* **POST** `/api/products/` - Add a new product (Requires authentication)
* **PUT** `/api/products/{id}/` - Update a product (Requires authentication)
* **DELETE** `/api/products/{id}/` - Delete a product (Requires authentication)
* **GET** `/api/orders/` - List all orders (Requires authentication)
* **POST** `/api/orders/` - Create a new order (Requires authentication)

## Tests

To run the test suite for the project:

```bash
python manage.py test
```

This will run all the unit tests defined in the project.

## Contributing

We welcome contributions! To contribute to this project:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-name).
3. Make your changes and commit them (git commit -am 'Add feature').
4. Push to your forked repository (git push origin feature-name).
5. Create a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
