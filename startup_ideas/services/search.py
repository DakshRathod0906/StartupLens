from dataclasses import dataclass
from typing import Optional
from django.db.models import QuerySet
from ..models import StartupIdea

@dataclass
class IdeaSearchFilter:
    keyword: Optional[str] = None
    industry_id: Optional[int] = None
    status: Optional[str] = None
    stage: Optional[str] = None
    owner: Optional[object] = None # Optional user instance to scope search
    
    # Exclude archived if false, or whatever logic needed
    include_archived: bool = False

class SearchService:
    @staticmethod
    def search(filters: IdeaSearchFilter) -> QuerySet:
        """
        Returns a lazy QuerySet of StartupIdeas matching the filters.
        """
        qs = StartupIdea.objects.all()
        
        if filters.owner:
            qs = qs.filter(owner=filters.owner)
            
        if not filters.include_archived:
            from ..constants import StartupIdeaStatus
            qs = qs.exclude(status=StartupIdeaStatus.ARCHIVED)
            
        # The query uses the manager's search method which implements icontains
        qs = qs.search(
            query=filters.keyword,
            industry_id=filters.industry_id,
            status=filters.status,
            stage=filters.stage
        )
        
        return qs
