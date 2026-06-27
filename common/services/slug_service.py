import uuid
from django.utils.text import slugify

class SlugService:
    @staticmethod
    def generate_slug(title: str, model_class, instance=None) -> str:
        """
        Generates a deterministic unique slug for a given model.
        e.g. my-ai-startup, my-ai-startup-2, my-ai-startup-3
        """
        base_slug = slugify(title)
        if not base_slug:
            base_slug = str(uuid.uuid4())[:8]
            
        slug = base_slug
        counter = 2
        
        while True:
            qs = model_class.objects.filter(slug=slug)
            if instance and instance.pk:
                qs = qs.exclude(pk=instance.pk)
                
            if not qs.exists():
                return slug
                
            slug = f"{base_slug}-{counter}"
            counter += 1
