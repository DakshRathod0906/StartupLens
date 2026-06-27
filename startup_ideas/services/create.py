from django.db import transaction
from ..models import StartupIdea
from common.services.slug_service import SlugService

class CreateService:
    @staticmethod
    @transaction.atomic
    def create_idea(owner, data: dict) -> StartupIdea:
        """
        Creates a new StartupIdea with a unique slug.
        Tags are handled separately if provided.
        """
        tags = data.pop('tags', [])
        
        title = data.get('title')
        slug = SlugService.generate_slug(title, StartupIdea)
        
        idea = StartupIdea(owner=owner, slug=slug, **data)
        idea.full_clean()
        idea.save()
        
        if tags:
            idea.tags.set(tags)
            
        return idea
