from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Class for the Base Custom User Manager
class UserManager(BaseUserManager):
    pass

# Class for the User model inheriting from AbstractUser
class User(AbstractUser):
    pass


# Class for the User Profile inheriting from models
class UserProfile(models.Model):
    pass