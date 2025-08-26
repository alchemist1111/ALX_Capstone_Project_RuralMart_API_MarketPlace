from django.test import TestCase
from accounts.models import User

class UserModelTestCase(TestCase):
    def test_create_user(self):
        # Test creating a regular user
        user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='johndoe@gmail.com',
            phone_number='1234567890',
            roles='buyer',
            password='Password123'
        )
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'johndoe@gmail.com')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.roles, 'buyer')
        self.assertTrue(user.check_password('Password123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        
    def test_create_superuser(self):
        # Test creating a superuser
        superuser = User.objects.create_superuser(
            first_name='Admin',
            last_name='User',
            email='adminuser@gmail.com',
            phone_number='1234567891',
            password='Password123'
        )
        self.assertEqual(superuser.email, 'adminuser@gmail.com')
        self.assertTrue(superuser.check_password('Password123'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        
    def test_create_user_with_invalid_email(self):
        # Test creating a user with invalid email
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name='Jane',
                last_name='Doe',
                email='',
                phone_number='1234567892',
                roles='buyer',
                password='Password123'
            )
    def test_user_roles(self):
        # Test the user roles choices
        user = User.objects.create_user(
            first_name='Alice',
            last_name='Smith',
            email='smithalice@gmail.com',
            phone_number='1234567893',
            roles='vendor',
            password='Password123'
        )
        self.assertEqual(user.roles, 'vendor')
        