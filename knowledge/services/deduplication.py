from ..models import Finding

class DeduplicationService:
    @staticmethod
    def is_duplicate(source_id: int, finding_type: str, normalized_title: str) -> bool:
        """
        Check if a finding of the same type and normalized title exists for this source.
        """
        return Finding.objects.filter(
            research_source_id=source_id,
            finding_type=finding_type,
            normalized_title=normalized_title
        ).exists()
