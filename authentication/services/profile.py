from django.db import transaction
from common.services.base import BaseService
from common.services.image_service import ImageService
from ..exceptions import ProfileUpdateError

class ProfileService(BaseService):
    """
    Handles updating user profile information, including images.
    """

    @staticmethod
    @transaction.atomic
    def update_profile(user, cleaned_data: dict):
        """
        Update the user's profile information.
        
        Args:
            user: The authenticated User instance.
            cleaned_data: Validated dictionary containing profile updates.
            
        Raises:
            ProfileUpdateError: If the profile update fails.
        """
        try:
            user.first_name = cleaned_data.get('first_name', user.first_name)
            user.last_name = cleaned_data.get('last_name', user.last_name)
            user.username = cleaned_data.get('username', user.username)
            user.bio = cleaned_data.get('bio', user.bio)
            
            # Handle profile picture upload
            new_picture = cleaned_data.get('profile_picture')
            
            # False indicates "clear the image"
            if new_picture is False:
                ImageService.delete_old_image(user.profile_picture)
                user.profile_picture = None
            elif new_picture:
                # Delete the old one if it exists
                ImageService.delete_old_image(user.profile_picture)
                
                # Process the new picture via ImageService
                processed_img = ImageService.process_profile_image(new_picture)
                user.profile_picture = processed_img
                
            user.save()
            return user
        except Exception as e:
            raise ProfileUpdateError(f"Failed to update profile: {str(e)}")
