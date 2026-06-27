from dataclasses import dataclass
from django.db.models import Count
from ..models import StartupIdea
from ..constants import StartupIdeaStatus

@dataclass
class DashboardMetrics:
    total: int
    draft: int
    published: int
    archived: int
    recent_ideas: list

class DashboardService:
    @staticmethod
    def get_dashboard_data(user) -> DashboardMetrics:
        """
        Aggregates dashboard metrics for the given user's startup ideas.
        """
        base_qs = StartupIdea.objects.owned_by(user)
        all_base_qs = StartupIdea.all_objects.owned_by(user).filter(is_deleted=False)
        
        total = base_qs.count()
        draft = base_qs.filter(status=StartupIdeaStatus.DRAFT).count()
        published = base_qs.filter(status=StartupIdeaStatus.PUBLISHED).count()
        archived = all_base_qs.filter(status=StartupIdeaStatus.ARCHIVED).count()
        
        recent_ideas = list(all_base_qs.order_by('-updated_at')[:5])
        
        return DashboardMetrics(
            total=total,
            draft=draft,
            published=published,
            archived=archived,
            recent_ideas=recent_ideas
        )
