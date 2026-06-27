import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, Context
from django.utils import timezone
from emails.models import NotificationQueue, EmailLog, NotificationPreference, NotificationTemplate

logger = logging.getLogger(__name__)


class EmailDeliveryService:
    """
    Synchronous email delivery using Django's built-in email backend.
    No Celery. No Redis. No background queues.
    """

    @staticmethod
    def send_notification(user, template: NotificationTemplate, context_data: dict) -> EmailLog:
        """
        Sends a single notification email synchronously.
        """
        # Check user preferences
        prefs, _ = NotificationPreference.objects.get_or_create(user=user)
        if template.name == 'weekly_summary' and not prefs.weekly_summary:
            logger.info(f"Skipping weekly_summary for {user.email} — preference disabled.")
            return None

        # Render templates
        subject = Template(template.subject_template).render(Context(context_data))
        body = Template(template.body_template).render(Context(context_data))

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            status = "SENT"
            logger.info(f"Email sent to {user.email}: {subject}")
        except Exception as e:
            status = "FAILED"
            logger.error(f"Email to {user.email} failed: {e}")

        # Log every attempt
        log = EmailLog.objects.create(
            recipient_email=user.email,
            subject=subject,
            body=body,
            status=status,
            sent_at=timezone.now() if status == "SENT" else None,
        )
        return log

    @staticmethod
    def send_welcome_email(user):
        """Convenience method for welcome emails."""
        template, _ = NotificationTemplate.objects.get_or_create(
            name="welcome",
            defaults={
                "subject_template": "Welcome to StartupLens, {{ user_name }}!",
                "body_template": "Hi {{ user_name }},\n\nWelcome to StartupLens — your startup validation platform.\n\nGet started by creating your first Startup Idea.",
            }
        )
        return EmailDeliveryService.send_notification(user, template, {"user_name": user.get_full_name() or user.username})

    @staticmethod
    def send_analysis_complete_email(user, startup_idea):
        """Convenience method for analysis-complete notifications."""
        template, _ = NotificationTemplate.objects.get_or_create(
            name="analysis_complete",
            defaults={
                "subject_template": "Your analysis for '{{ idea_title }}' is ready",
                "body_template": "Hi {{ user_name }},\n\nThe full evaluation for '{{ idea_title }}' has been completed.\n\nLog in to view your report.",
            }
        )
        return EmailDeliveryService.send_notification(user, template, {
            "user_name": user.get_full_name() or user.username,
            "idea_title": startup_idea.title,
        })

    @staticmethod
    def send_report_ready_email(user, startup_idea):
        """Convenience method for report-ready notifications."""
        template, _ = NotificationTemplate.objects.get_or_create(
            name="report_ready",
            defaults={
                "subject_template": "Your PDF report for '{{ idea_title }}' is ready to download",
                "body_template": "Hi {{ user_name }},\n\nYour executive report for '{{ idea_title }}' has been generated.\n\nLog in to download the PDF.",
            }
        )
        return EmailDeliveryService.send_notification(user, template, {
            "user_name": user.get_full_name() or user.username,
            "idea_title": startup_idea.title,
        })
