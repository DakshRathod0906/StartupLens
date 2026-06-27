from django.contrib.auth.mixins import AccessMixin
from .models import UserRole

class RoleRequiredMixin(AccessMixin):
    """
    Verify that the current user has specific roles.
    """
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in self.allowed_roles:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class AdminRequiredMixin(RoleRequiredMixin):
    """
    Verify that the current user is an admin.
    """
    allowed_roles = [UserRole.ADMIN]
