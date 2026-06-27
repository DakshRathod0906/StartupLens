import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import validate_username_format, validate_image_size, validate_image_extension
from .managers import UserManager


def profile_picture_upload_path(instance, filename):
    folder = instance.id if instance.id else uuid.uuid4().hex
    return f"profile_pictures/{folder}/{filename}"


class UserRole(models.TextChoices):
    USER = "USER", _("User")
    ADMIN = "ADMIN", _("Admin")


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Adds additional StartupLens-specific fields.
    """
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        validators=[validate_username_format],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    
    profile_picture = models.ImageField(
        upload_to=profile_picture_upload_path,
        blank=True,
        null=True,
        validators=[validate_image_size, validate_image_extension]
    )
    bio = models.TextField(blank=True, max_length=500)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    
    is_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class UserLoginHistory(models.Model):
    """
    Tracks user login events for auditing and security.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    login_at = models.DateTimeField(auto_now_add=True)
    successful_login = models.BooleanField(default=True)

    class Meta:
        ordering = ["-login_at"]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['login_at']),
            models.Index(fields=['successful_login']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.login_at} - {'Success' if self.successful_login else 'Failed'}"
