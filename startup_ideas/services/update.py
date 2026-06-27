from django.db import transaction
from django.core.exceptions import PermissionDenied
from ..models import StartupIdea
from ..exceptions import VersionConflictError

class UpdateService:
    @staticmethod
    @transaction.atomic
    def update_idea(user, idea: StartupIdea, data: dict, submitted_version: int) -> StartupIdea:
        """
        Updates a StartupIdea with optimistic locking.
        """
        if idea.owner != user:
            raise PermissionDenied("You do not have permission to edit this idea.")
            
        # Refresh from db to get current version
        idea.refresh_from_db(fields=['version'])
        
        if idea.version != submitted_version:
            raise VersionConflictError(
                "This idea was modified by someone else (or in another tab) since you opened it. "
                "Please refresh and try again."
            )
            
        tags = data.pop('tags', None)
        
        for key, value in data.items():
            setattr(idea, key, value)
            
        # Increment version
        idea.version += 1
        
        idea.full_clean()
        idea.save()
        
        if tags is not None:
            idea.tags.set(tags)
            
        return idea
