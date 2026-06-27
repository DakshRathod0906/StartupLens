from django.test import TestCase
from django.contrib.auth import get_user_model
from authentication.services.registration import RegistrationService
from authentication.services.login import LoginService
from authentication.services.profile import ProfileService
from authentication.services.password import PasswordService
from authentication.exceptions import RegistrationError, LoginError
from django.http import HttpRequest
from django.contrib.sessions.middleware import SessionMiddleware

User = get_user_model()

class RegistrationServiceTests(TestCase):
    def test_register_user_success(self):
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser123',
            'password': 'StrongPassword123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        user = RegistrationService.register_user(data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.username, 'newuser123')
        
    def test_register_user_duplicate_email(self):
        User.objects.create_user(email='existing@example.com', username='u1', password='p1')
        data = {
            'email': 'existing@example.com',
            'username': 'newuser123',
            'password': 'StrongPassword123!',
        }
        with self.assertRaises(RegistrationError):
            RegistrationService.register_user(data)

class LoginServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='loginuser@example.com',
            username='loginuser',
            password='loginpass123'
        )
        self.request = HttpRequest()
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(self.request)
        self.request.session.save()

    def test_login_success_with_username(self):
        user = LoginService.login_user(self.request, 'loginuser', 'loginpass123')
        self.assertEqual(user, self.user)
        self.assertIn('_auth_user_id', self.request.session)

    def test_login_success_with_email(self):
        user = LoginService.login_user(self.request, 'loginuser@example.com', 'loginpass123')
        self.assertEqual(user, self.user)

    def test_login_failure(self):
        with self.assertRaises(LoginError):
            LoginService.login_user(self.request, 'loginuser', 'wrongpass')

class ProfileServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='profile@example.com',
            username='profile',
            password='p1'
        )

    def test_update_profile(self):
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'New bio',
        }
        user = ProfileService.update_profile(self.user, data)
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.bio, 'New bio')

class PasswordServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='password@example.com',
            username='passworduser',
            password='oldpassword'
        )
        self.request = HttpRequest()
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(self.request)
        self.request.session.save()

    def test_change_password(self):
        PasswordService.change_password(self.user, self.request, 'newpassword')
        self.assertTrue(self.user.check_password('newpassword'))
