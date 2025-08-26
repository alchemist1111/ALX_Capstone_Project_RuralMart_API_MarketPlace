from rest_framework import status
from .tokens import generate_tokens
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from .tokens import blacklist_token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .serializers import UserRegistrationSerializer, UserSerializer, UserUpdateSerializer, UserProfileSerializer
from .permissions import IsAdminUser
from .models import UserProfile
from rest_framework import generics
from django.contrib.auth import get_user_model  

User = get_user_model()

# User CRUD
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
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        # Extract email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if email and password are provided
        if not email or not password:
            raise ValidationError("Email and password are required fields.")
            
        try:
            # Get the user by email
            user = User.objects.get(email=email)   
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)    
        
        # Check the password manually
        if not user.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate the tokens for the authenticated user
        if user and check_password(password, user.password):
            # Create JWT tokens for the authenticated user
            token = generate_tokens(user)
            
            # Return response with tokens and user details
            return Response(
                {
                    'refresh': token['refresh'],
                    'access': token['access'],
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
        
        
# Class for user logout
class UserLogoutView(APIView):
    """
    Handles user logout.
    - Blacklists the refresh token so it cannot be used for further authentication.
    """      
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        """
        Handle logout by blacklisting the refresh token.
        """
        # Access the user's refresh token from the request
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({'error': 'Refresh token is required for logout.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Call the function to blacklist the refresh token
        if blacklist_token(refresh_token):
            return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid refresh token or error blacklisting token.'}, status=status.HTTP_400_BAD_REQUEST)   



# User list view
class UserListView(ListAPIView):
    """
       List all users but only for admin users.
    
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]
    


# User details view
class UserDetailView(RetrieveAPIView):
    """
       Retrieve a single user by ID.
    
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'

# User update view
class UserUpdateView(UpdateAPIView):
    """
      Update a user by ID.
    
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def get_object(self):
        """
           A user to only update their own details.
        """
        user = super().get_object()
        if user != self.request.user:
            raise PermissionDenied("You can only update your own account.")
        return user

# User delete view
class UserDeleteView(DestroyAPIView):
    """
      Delete a user by ID.
    """ 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]  
    lookup_field = 'pk'
    
# User profile [C]RUD
# User profile list & create
class UserProfileListView(generics.ListCreateAPIView):
    """
       List all user profiles or create a new profile.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        # Automatically associate the logged-in user with the profile when creating
        serializer.save(user=self.request.user)
        
# User profile retrieve, update & delete
class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
       Retrieve, update, or delete a user profile.
    """ 
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'      
            
             
            
         