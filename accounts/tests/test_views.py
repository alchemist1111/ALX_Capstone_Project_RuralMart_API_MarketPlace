from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()

# Test cases for user views
class UserViewsTestCase(APITestCase):
    def setUp(self):
        # Create a test admin user
        self.admin_user = User.objects.create_user(
            email='admin@gmail.com',
            password='Admin@123'
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        
        # Create a test regular user
        self.regular_user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='johndoe@gmail.com',
            phone_number='1234567890',
            roles='buyer',
            password='RegularUser@123'
        )
        self.regular_user.save()
        
        # Create a UserProfile for the admin user if needed
        self.user_profile = UserProfile.objects.create(user=self.admin_user)
    
    def test_user_list_view_as_admin(self):
        """
        Test that an admin user can access the user list.
        """
        url = '/users/auth/list/'
        #Login as admin
        self.client.login(
            email='admin@gmail.com',
            password='Admin@123'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return both users
        
    def test_user_list_view_as_regular_user(self):
        """
        Test that a regular user cannot access the user list.
        """ 
        url = '/users/auth/list/'
        #Login as regular user
        self.client.login(
            email='johndoe@gmail.com',
            password='RegularUser@123'
        )        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_user_detail_view(self):
        """
        Test that an admin can retrieve a user by ID.
        """
        url = f'/users/auth/detail/{self.regular_user.pk}/'
        # Login as admin
        self.client.login(
            email='admin@gmail.com',
            password='Admin@123'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'admin')
        
    def test_user_update_view(self):
        """
        Test that a user can update their own details.
        """
        url = f'/users/auth/update/{self.regular_user.pk}/'
        new_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '0987654321',
            'roles': 'seller'
        }    
        # Login as regular user
        self.client.login(
            email='janedoe@gmail.com',
            password='RegularUser@123'
        )
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Jane')
    
    def test_user_update_view_permission_denied(self):
        """
        Test that a user cannot update another user's details.
        """
        url = f'/users/auth/update/{self.regular_user.pk}/'
        new_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '0987654321',
            'roles': 'seller'
        }    
        # Login as admin user
        self.client.login(
            email='janedoe@gmail.com',
            password='RegularUser@123'
        )
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_user_delete_view(self):
        """
        Test that an admin can delete a user.
        """
        url = f'/users/auth/delete/{self.regular_user.pk}/'
        
        # Login as admin user
        self.client.login(
            email='admin@gmail.com',
            password='Admin@123'
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.regular_user.pk).exists())
        
    def test_user_profile_list_view_as_admin(self):
        """
        Test that an admin user can list all user profiles.
        """
        url = '/users/auth/profiles/'
        
        # Login as admin user
        self.client.login(
            email='admin@gmail.com',
            password='Admin@123'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one profile created in setUp
        
    def test_user_profile_create_view(self):
        """
        Test that an admin user can create own user profile.
        """
        url = '/users/auth/profiles/'
        
        # Login as admin user
        self.client.login(
            email='admin@gmail.com',
            password='Admin@123'
        )
        
        # New profile data
        new_profile_data = {
            'user': self.admin_user.id,
            'bio': 'Admin user bio',
        }
        response = self.client.post(url, new_profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.admin_user.id)
        
    def test_user_profile_detail_view(self):
        """
        Test that an admin can retrieve a user profile by ID.
        """
        url = f'/users/auth/profiles/{self.user_profile.pk}/'
        
        # Login as admin user
        self.client.login(
            email='admin@gmail.com',
            password='Admin@123'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.admin_user.id)
        
    def test_user_profile_update_view(self):
        """
        Test that an admin can update a user profile.
        """
        url = f'/users/auth/profiles/{self.user_profile.pk}/'
        
        # Login as admin user
        self.client.login(
            email='admin@gmail.com',
            password='Admin@123'
        )
        updated_data = {
            'bio': 'Updated admin bio',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Updated admin bio')
        
            