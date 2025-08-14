from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# User profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        
        
# User registration serializer
class UserSerializer(serializers.ModelSerializer):
    """
      Handles sign up for the custom model
      - Accepts optional nested `userprofile` to create a profile together with the user.
      - Enforces password confirmation and Django's password validators.
    
    """
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
    userprofile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'roles', "password", "password2", "userprofile"]
        extra_kwargs = {"roles": {"default": "buyer"}}
    
    def validate(self, data):
        """
           Ensuring that the two password fields match and validate password strength.
           
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        validate_password(data['password'])
        return data
    
    def create(self, validated_data):
        """
          Create user and associated profile if provided.
          
        """
        userprofile_data = validated_data.pop('userprofile', None)
        user = User.objects.create_user(**validated_data)
        
        if userprofile_data:
            UserProfile.objects.create(user=user, **userprofile_data)

        return user
            
# User registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'roles', 'password']  
    
    def create(self, validated_data):
        """
          Create and return a new user instance, with hashed password.
        
        """
        password = password = validated_data.pop('password')  # Extract the password from validated data
        user = User(**validated_data) # Create user object without saving to DB yet
        user.set_password(password) # Hash the password for security
        try:
            user.save() # Save the user to the database
        except Exception as e:
            raise ValidationError(f"Error saving user: {e}")
        return user # Return the user instance        