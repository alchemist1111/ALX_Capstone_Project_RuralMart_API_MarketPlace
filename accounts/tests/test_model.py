from django.test import TestCase
from accounts.models import User, UserProfile

# Test cases for the custom User model
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


# Test cases for the user profile model
class UserProfileModelTestCase(TestCase):
    # Create a user
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='testuser@gmail.com',
            phone_number='1234567894',
            roles='buyer',
            password='Password123'
        )
        # Ensure only one profile exists for the user
        self.profile, created = UserProfile.objects.get_or_create(
            user=self.user,
            defaults={'address': '123 Test St, Test City', 'bio': 'This is a test bio.'}
        )
        if not created:
            self.profile.address = '123 Test St, Test City'
            self.profile.bio = 'This is a test bio.'
            self.profile.save()
    
    def test_create_user_profile(self):
        # Check if the UserProfile is correctly created
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.address, '123 Test St, Test City')
        self.assertEqual(self.profile.bio, 'This is a test bio.')
    
    def test_profile_str_method(self):
        # Check if the __str__ method is correct
        self.assertEqual(str(self.profile), f"Profile of {self.user.first_name} {self.user.last_name}")
    
    def test_user_profile_relation(self):
        # Ensure the user has a user profile
        self.assertTrue(hasattr(self.user, 'userprofile'))

# # Test cases for the relationship between User and UserProfile
# class UserProfileRelationTestCase(TestCase):

#     def setUp(self):
#         # Create a user and their profile
#         self.user = User.objects.create_user(
#             email='user@example.com',
#             password='password123',
#             first_name='John',
#             last_name='Doe',
#             phone_number='+254700000000',
#             roles='buyer'
#         )
#         self.profile = UserProfile.objects.create(
#             user=self.user,
#             address="Test Address",
#             bio="Test Bio"
#         )

#     def test_user_profile_association(self):
#         # Ensure a profile is created for the user
#         self.assertEqual(self.profile.user, self.user)

#     def test_user_profile_creation_on_user_creation(self):
#         # Ensure that when the user is created, a profile is created for them
#         user = User.objects.create_user(
#             email='newuser@example.com',
#             password='password123',
#             first_name='Jane',
#             last_name='Doe',
#             phone_number='+254700000001',
#             roles='vendor'
#         )
#         self.assertTrue(hasattr(user, 'userprofile'))

        
        