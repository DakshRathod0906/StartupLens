from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from ..models import StartupIdea
from ..constants import StartupIdeaStatus

class ArchiveService:
    @staticmethod
    @transaction.atomic
    def archive_idea(user, idea: StartupIdea) -> StartupIdea:
        if idea.owner != user:
            raise PermissionDenied("You do not have permission to archive this idea.")
            
        idea.status = StartupIdeaStatus.ARCHIVED
        idea.is_archived = True
        idea.archived_at = timezone.now()
        idea.save(update_fields=['status', 'is_archived', 'archived_at', 'updated_at'])
        return idea
