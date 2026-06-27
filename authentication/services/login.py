from django.contrib.auth import authenticate, login
from common.services.base import BaseService
from ..exceptions import LoginError

class LoginService(BaseService):
    """
    Handles user authentication and login logic.
    """
    
    @staticmethod
    def login_user(request, username: str, password: str, remember_me: bool = False):
        """
        Authenticate and log a user in.
        
        Args:
            request: The HTTP request object.
            username: The provided username or email.
            password: The provided password.
            remember_me: Whether to extend the session expiry.
            
        Returns:
            The authenticated User instance.
            
        Raises:
            LoginError: If credentials are invalid or the account is disabled.
        """
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise LoginError("Invalid username or password.")
            
        if not user.is_active:
            raise LoginError("This account is inactive.")
            
        login(request, user)
        
        if not remember_me:
            request.session.set_expiry(0)  # Expires when the browser is closed
            
        return user
