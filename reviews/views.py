from rest_framework import viewsets
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        """
            Optionally restricts the returned reviews to a given user,
            by filtering against a 'user' query parameter in the URL.
            If the user is not authenticated, return an empty queryset.
        """
        user = self.request.user
        
        # If user is not authenticated, return an empty queryset
        if user.is_anonymous:
            return Review.objects.none()
        
        queryset = Review.objects.all()
        product_id = self.request.query_params.get('product', None)
        
        if product_id:
            queryset = queryset.filter(product__id=product_id)
        return queryset.filter(user=user)
    
    def perform_create(self, serializer):
        """
           Overriding this method to automatically set the logged-in user for the review.
        """
        serializer.save(user=self.request.user)
        
    def update(self, request, *args, **kwargs):
        """
        Override update method to ensure user and product cannot be changed.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "You do not have permission to edit this review."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)  
    
    def create(self, request, *args, **kwargs):
        """
            Ensure the user is authenticated before creating a review.
            If unauthenticated, return an empty queryset and a message prompting login/signup.
        """
        user = request.user 
        
        # If the user is not authenticated, return a 401 Unauthorized response
        if user.is_anonymous:
            return Response(
                {"detail": "You must be logged in to create a review. Please log in or sign up."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # if user.is_anonymous:
        #     # Redirect to login or signup page based on some condition
        #     return redirect('/login/') 
        return super().create(request, *args, **kwargs)
