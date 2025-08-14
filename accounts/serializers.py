from rest_framework import serializers
from .models import User, UserProfile


# User registration serializer
class UserSerializer(serializers.ModelSerializer):
    """
      Handles sign up for the custom model
      - Accepts optional nested `userprofile` to create a profile together with the user.
      - Enforces password confirmation and Django's password validators.
    
    """
    # password = serializers.CharField(write_only=True, style={"input_type": "password"})
    # password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
    # userprofile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['email', 'first_name', 'last_name', 'phone_number', 'roles', "password", "password2", "userprofile"]
        # extra_kwargs = {"roles": {"default": "buyer"}}
        
# User registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'roles']        