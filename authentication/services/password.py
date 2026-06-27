from django.db import transaction
from django.contrib.auth import update_session_auth_hash
from common.services.base import BaseService
from ..exceptions import PasswordUpdateError

class PasswordService(BaseService):
    """
    Handles user password changes and management.
    """

    @staticmethod
    @transaction.atomic
    def change_password(user, request, new_password: str):
        """
        Change the user's password and update the session auth hash
        so they are not logged out.
        
        Args:
            user: The authenticated User instance.
            request: The HTTP request object.
            new_password: The validated new password.
            
        Raises:
            PasswordUpdateError: If the password update fails.
        """
        try:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
        except Exception as e:
            raise PasswordUpdateError(f"Failed to change password: {str(e)}")
