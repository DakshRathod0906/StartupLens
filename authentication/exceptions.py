class AuthenticationError(Exception):
    """Base exception for authentication-related errors."""
    pass

class RegistrationError(AuthenticationError):
    """Raised when user registration fails."""
    pass

class LoginError(AuthenticationError):
    """Raised when user login fails."""
    pass

class ProfileUpdateError(AuthenticationError):
    """Raised when updating user profile fails."""
    pass

class PasswordUpdateError(AuthenticationError):
    """Raised when updating user password fails."""
    pass
