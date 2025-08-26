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
 
