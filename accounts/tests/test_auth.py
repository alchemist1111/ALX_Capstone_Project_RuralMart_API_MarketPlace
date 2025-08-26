from rest_framework.test import APITestCase
from rest_framework import status

# User Registration Test Case
class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        url = '/users/auth/register/'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@gmail.com',
            'phone_number': '+254797086131',
            'roles': 'buyer',
            'password': 'Password@123'      
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('The user registered successfully.', str(response.data))
        
# User Login Test Case
class UserLoginTestCase(APITestCase):
    # Register the user first
    def setUp(self):
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@gmail.com',
            'phone_number': '+254797086131',
            'roles': 'buyer',
            'password': 'Password@123'
        } 
        self.client.post('/users/auth/register/', self.user_data, format='json')   
        
    def test_login_success(self):
        url = '/users/auth/login/'
        login_data = {
            'email': 'johndoe@gmail.com',
            'password': 'Password@123'
        }
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user', str(response.data))  
        
    def test_login_failure(self):
        url = '/users/auth/login/'
        login_data = {
            'email': 'johndoe@gmail.com',
            'password': 'WrongPassword'  # Incorrect password
        }
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  
        self.assertIn('Invalid email or password', str(response.data))


# User logout Test Case
class UserLogoutTestCase(APITestCase):
    def setUp(self):
        # Register the user first
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@gmail.com',
            'phone_number': '+254797086131',
            'roles': 'buyer',
            'password': 'Password@123'
        } 
        self.client.post('/users/auth/register/', self.user_data, format='json')  

        # Log in the user to get the tokens
        login_data = {
            'email': 'johndoe@gmail.com',
            'password': 'Password@123'
        }
        login_response = self.client.post('/users/auth/login/', login_data, format='json')

        self.access_token = login_response.data['access']  # Save the access token for authentication
        self.refresh_token = login_response.data['refresh']  # Save the refresh token for logout

    def test_logout_success(self):
        url = '/users/auth/logout/'
        data = {
            'refresh': self.refresh_token  # Include the refresh token in the logout request
        }
        headers = {'Authorization': f'Bearer {self.access_token}'}  # Add the access token for authentication
        response = self.client.post(url, data, format='json', **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'})

        # Log the response for debugging
        print(f"Response data: {response.data}")

        # Check if the logout was successful
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('User logged out successfully', str(response.data))

    def test_logout_failure_no_refresh_token(self):
        url = '/users/auth/logout/'
        headers = {'Authorization': f'Bearer {self.access_token}'}  # Add the access token for authentication
        response = self.client.post(url, headers=headers, format='json', **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'})  # No refresh token provided
        
        # Check if it returns the correct error message when no refresh token is provided
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Refresh token is required for logout', str(response.data))

    def test_logout_failure_invalid_refresh_token(self):
        url = '/users/auth/logout/'
        invalid_refresh_token = 'invalid_refresh_token'
        data = {
            'refresh': invalid_refresh_token  # Provide an invalid refresh token
        }
        headers = {'Authorization': f'Bearer {self.access_token}'}  # Add the access token for authentication
        response = self.client.post(url, data, format='json', **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'})

        # Log the response for debugging
        print(f"Response data: {response.data}")

        # Check if it returns the correct error message when an invalid refresh token is provided
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid refresh token or error blacklisting token', str(response.data))
 
