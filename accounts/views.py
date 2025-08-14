from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
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
