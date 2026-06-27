from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from ..models import StartupIdea

class DeleteService:
    @staticmethod
    @transaction.atomic
    def soft_delete_idea(user, idea: StartupIdea) -> StartupIdea:
        if idea.owner != user:
            raise PermissionDenied("You do not have permission to delete this idea.")
            
        idea.is_deleted = True
        idea.deleted_at = timezone.now()
        idea.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
        return idea
