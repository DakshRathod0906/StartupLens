from functools import wraps
from django.core.exceptions import PermissionDenied
from .models import UserRole

def role_required(allowed_roles):
    """
    Decorator for views that checks whether a user has a particular role,
    raising PermissionDenied if necessary.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def admin_required():
    """
    Decorator for views that checks that the user is an admin,
    raising PermissionDenied if necessary.
    """
    return role_required([UserRole.ADMIN])
