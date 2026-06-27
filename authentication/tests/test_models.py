from django.test import TestCase
from django.contrib.auth import get_user_model
from authentication.models import UserLoginHistory

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_verified)
        self.assertEqual(user.role, 'USER')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='adminuser',
            password='adminpassword123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.role, 'ADMIN')

    def test_email_normalization(self):
        user = User.objects.create_user(
            email='TEST@EXAMPLE.COM',
            username='testuser2',
            password='password123'
        )
        self.assertEqual(user.email, 'TEST@example.com')

    def test_user_str(self):
        user = User.objects.create_user(
            email='teststr@example.com',
            username='struser',
            password='password'
        )
        self.assertEqual(str(user), 'teststr@example.com')


class UserLoginHistoryTests(TestCase):
    def test_create_history(self):
        user = User.objects.create_user(email='test@ex.com', username='testu', password='123')
        history = UserLoginHistory.objects.create(
            user=user,
            ip_address='127.0.0.1',
            user_agent='Mozilla/5.0',
            successful_login=True
        )
        self.assertEqual(history.user, user)
        self.assertEqual(history.ip_address, '127.0.0.1')
        self.assertTrue(history.successful_login)
        self.assertIn('test@ex.com', str(history))
