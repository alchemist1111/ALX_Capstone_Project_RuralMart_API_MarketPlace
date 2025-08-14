from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from .serializers import UserRegistrationSerializer

# Class for user registration
class UserRegistrationView(CreateAPIView):
    """
        Handles user registration.
        - Takes data from the request body and creates a new user in the system.
        - Returns user data on successful registration.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
          Handles the POST request to register a new user.
          
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {
                "message": "The user registered successfully.",
                "user": serializer.data
            }
            return Response(message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Class for user login view
class UserLoginView(APIView):
    """
        Handles user login.
        - Authenticates the user with email and password.
        - Returns JWT tokens (access and refresh tokens) on successful login.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        # Extract email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if email and password are provided
        if not email or not password:
            raise ValidationError("Email and password are required fields.")
            
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Create JWT tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            
            # Return response with tokens and user details
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'roles': user.roles
                    }
                },
                status=status.HTTP_200_OK
            )
        # If authentication fails, return an error message    
        return Response(
            {'detail': 'Incorrect email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
        