from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    
    # Use the settings for token expiration times
    refresh.set_exp(lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
    refresh.access_token.set_exp(lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }