import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from .constants import MAX_PROFILE_IMAGE_SIZE, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH

def validate_username_format(value):
    """
    Validate that the username contains only letters, numbers, underscores, and dots.
    No spaces or other special characters are allowed.
    """
    if len(value) < USERNAME_MIN_LENGTH or len(value) > USERNAME_MAX_LENGTH:
        raise ValidationError(
            _(f"Username must be between {USERNAME_MIN_LENGTH} and {USERNAME_MAX_LENGTH} characters.")
        )
        
    if not re.match(r'^[a-zA-Z0-9_\.]+$', value):
        raise ValidationError(
            _("Username can only contain letters, numbers, underscores, and dots. No spaces allowed.")
        )

def validate_image_size(image):
    """
    Validate that the uploaded image size does not exceed the maximum allowed limit.
    """
    if image.size > MAX_PROFILE_IMAGE_SIZE:
        max_size_mb = MAX_PROFILE_IMAGE_SIZE / (1024 * 1024)
        raise ValidationError(
            _(f"Image size must not exceed {max_size_mb} MB.")
        )

def validate_image_extension(image):
    """
    Validate that the uploaded image has an allowed extension.
    """
    ext = os.path.splitext(image.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError(
            _(f"Unsupported file extension. Allowed extensions are: {', '.join(valid_extensions)}")
        )
