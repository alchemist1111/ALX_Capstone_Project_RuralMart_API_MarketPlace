from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Class for the Base Custom User Manager
class UserManager(BaseUserManager):
    pass

# Class for the User model inheriting from AbstractUser
class User(AbstractUser):
    # User roles
    USER_ROLES = (
        ('buyer', 'Buyer'),
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
    )
    username = None # Overriding the default username field
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, unique=True)
    roles = models.CharField(max_length=50, choices=USER_ROLES, default='buyer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True) 
    
    # Fields for use
    USERNAME_FIELD = 'email' # Use email for authentication, not username
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager() # Use the custon user manager
    
    def __str__(self):
        return f'Name:{self.first_name} {self.last_name}, Email:{self.email}'


# Class for the User Profile inheriting from models
class UserProfile(models.Model):
    pass