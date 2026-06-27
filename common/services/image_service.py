import os
import uuid
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from .base import BaseService


class ImageService(BaseService):
    """
    Service for handling image manipulation such as resizing, format conversion,
    and compression.
    """

    @staticmethod
    def process_profile_image(image_file, max_size=(512, 512), quality=85) -> InMemoryUploadedFile:
        """
        Process an uploaded profile image: resize it to max_size, convert it to WebP format,
        and compress it to the specified quality. Generates a deterministic UUID-based filename.
        
        Args:
            image_file: The uploaded image file.
            max_size: A tuple (width, height) specifying maximum dimensions.
            quality: Quality percentage for compression.
            
        Returns:
            An InMemoryUploadedFile containing the processed WebP image.
        """
        img = Image.open(image_file)
        
        # Convert to RGB if needed to avoid issues with saving as WebP
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGBA')

        # Resize the image using thumbnail (preserves aspect ratio)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to BytesIO in WebP format
        output_io = BytesIO()
        img.save(output_io, format='WEBP', quality=quality)
        output_io.seek(0)
        
        # Generate new filename
        new_filename = f"avatar_{uuid.uuid4().hex}.webp"
        
        # Create a new InMemoryUploadedFile
        processed_file = InMemoryUploadedFile(
            file=output_io,
            field_name='profile_picture',
            name=new_filename,
            content_type='image/webp',
            size=output_io.getbuffer().nbytes,
            charset=None
        )
        
        return processed_file

    @staticmethod
    def delete_old_image(image_field):
        """
        Delete an image file from storage if it exists.
        
        Args:
            image_field: The ImageFieldFile instance attached to a model.
        """
        if image_field and hasattr(image_field, 'path') and os.path.isfile(image_field.path):
            os.remove(image_field.path)
