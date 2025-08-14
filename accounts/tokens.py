from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    
    # Use the settings for token expiration times
    refresh.set_exp(lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
    refresh.access_token.set_exp(lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
    
# Function to blacklist token
def blacklist_token(refresh_token):
    """
        Blacklist the provided refresh token.
        This ensures that the refresh token cannot be used to get new access tokens.
        
    """ 
    try:
        # Create the refresh token instance from the provided refresh token
        token = RefreshToken(refresh_token)
        
        # Blacklist the refresh token
        token.blacklist()
        
        return True  # Successfully blacklisted the token
    except Exception as e:
        print(f"Error blacklisting token: {str(e)}")
        return False   