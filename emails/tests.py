from django.test import TestCase
from django.contrib.auth import get_user_model
from emails.models import NotificationPreference, NotificationTemplate, EmailLog

User = get_user_model()


class EmailModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', username='testuser', password='testpass123'
        )

    def test_notification_preference_defaults(self):
        pref = NotificationPreference.objects.create(user=self.user)
        self.assertTrue(pref.analysis_complete)
        self.assertTrue(pref.weekly_summary)
        self.assertFalse(pref.marketing)
        self.assertTrue(pref.investor_matches)

    def test_notification_template_creation(self):
        template = NotificationTemplate.objects.create(
            name='welcome',
            subject_template='Welcome {{ name }}',
            body_template='Hello {{ name }}, welcome!',
        )
        self.assertEqual(str(template), 'welcome')
        self.assertTrue(template.is_active)

    def test_email_log_creation(self):
        log = EmailLog.objects.create(
            recipient_email='test@example.com',
            subject='Test Subject',
            body='Test Body',
            status='SENT',
        )
        self.assertIn('test@example.com', str(log))


class EmailDeliveryServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', username='testuser', password='testpass123'
        )

    def test_send_welcome_email(self):
        from emails.services.delivery import EmailDeliveryService
        log = EmailDeliveryService.send_welcome_email(self.user)
        self.assertIsNotNone(log)
        self.assertEqual(log.status, 'SENT')
        self.assertEqual(log.recipient_email, 'test@example.com')

    def test_send_notification_respects_preferences(self):
        from emails.services.delivery import EmailDeliveryService
        pref = NotificationPreference.objects.create(user=self.user, weekly_summary=False)
        template = NotificationTemplate.objects.create(
            name='weekly_summary',
            subject_template='Weekly Summary',
            body_template='Your weekly summary.',
        )
        result = EmailDeliveryService.send_notification(self.user, template, {})
        self.assertIsNone(result)
