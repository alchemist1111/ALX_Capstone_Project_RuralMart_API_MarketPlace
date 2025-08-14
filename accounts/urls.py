from django.urls import path
from .views import UserRegistrationView

urlpatterns = [
    # Registration
    path('register/', UserRegistrationView.as_view(), name='register'),
]