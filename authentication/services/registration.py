from django.db import transaction
from django.contrib.auth import get_user_model
from common.services.base import BaseService
from ..exceptions import RegistrationError

User = get_user_model()

class RegistrationService(BaseService):
    """
    Handles user registration logic.
    """
    
    @staticmethod
    @transaction.atomic
    def register_user(cleaned_data: dict) -> User:
        """
        Create a new user account with the given data.
        
        Args:
            cleaned_data: Dictionary containing validated user data 
                          (email, username, password, first_name, last_name).
                          
        Returns:
            The created User instance.
            
        Raises:
            RegistrationError: If an error occurs during registration.
        """
        try:
            user = User.objects.create_user(
                email=cleaned_data['email'],
                username=cleaned_data['username'],
                password=cleaned_data['password'],
                first_name=cleaned_data.get('first_name', ''),
                last_name=cleaned_data.get('last_name', '')
            )
            return user
        except Exception as e:
            raise RegistrationError(f"Failed to register user: {str(e)}")
