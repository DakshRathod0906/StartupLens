from django.db import transaction
from django.core.exceptions import PermissionDenied
from ..models import StartupIdea
from ..constants import StartupIdeaStatus

class RestoreService:
    @staticmethod
    @transaction.atomic
    def restore_idea(user, idea: StartupIdea) -> StartupIdea:
        if idea.owner != user:
            raise PermissionDenied("You do not have permission to restore this idea.")
            
        idea.status = StartupIdeaStatus.DRAFT
        idea.is_archived = False
        idea.archived_at = None
        idea.save(update_fields=['status', 'is_archived', 'archived_at', 'updated_at'])
        return idea
