from django.db import models
from ..models import ResearchSource
from ..constants import ResearchSourceStatus

class DeduplicationService:
    @staticmethod
    def is_duplicate(job_id: int, canonical_url: str, content_hash: str) -> bool:
        """
        Checks if a source already exists for the given job.
        A duplicate is either the exact same canonical URL, or the exact same content hash.
        """
        return ResearchSource.objects.filter(
            research_job_id=job_id
        ).exclude(
            status=ResearchSourceStatus.FAILED
        ).filter(
            models.Q(canonical_url=canonical_url) | models.Q(content_hash=content_hash)
        ).exists()
