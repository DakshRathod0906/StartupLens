from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserLoginHistory
from .utils import get_client_ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Signal handler that records a login event to UserLoginHistory
    whenever a user successfully logs in.
    """
    if request:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        UserLoginHistory.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            successful_login=True
        )
