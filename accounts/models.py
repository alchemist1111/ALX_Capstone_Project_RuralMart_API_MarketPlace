from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.contrib.auth.models import get_user_model
from django.conf import settings

# User = get_user_model() # Call the function to get user model defined

# Class for the Base Custom User Manager
class UserManager(BaseUserManager):
    """"
         Create and return a user with an email and password.
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    # Create a super user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    address = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.first_name} {self.user.last_name}" 