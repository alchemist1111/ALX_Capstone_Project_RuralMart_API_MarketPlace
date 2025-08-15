from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserListView, UserDetailView, UserUpdateView, UserDeleteView, UserProfileDetailView, UserProfileListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Registration
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # List
    path('list/', UserListView.as_view(), name='user-list'),
    
    # Single user
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # User update
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    
    # User delete
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    
    # Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile
    path('profiles/', UserProfileListView.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),
]