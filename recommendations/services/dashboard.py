from dataclasses import dataclass
from ..models import Recommendation, RecommendationStatus
from .statistics import StatisticsService

@dataclass
class RecommendationStatistics:
    total_recommendations: int
    critical: int
    high: int
    medium: int
    low: int
    optional: int
    resolved_count: int

class DashboardService:
    @staticmethod
    def get_statistics() -> RecommendationStatistics:
        active_recs = Recommendation.objects.filter(status=RecommendationStatus.ACTIVE)
        
        total = active_recs.count()
        resolved = active_recs.filter(is_resolved=True).count()
        
        dist = StatisticsService.get_priority_distribution()
        
        return RecommendationStatistics(
            total_recommendations=total,
            critical=dist.get('CRITICAL', 0),
            high=dist.get('HIGH', 0),
            medium=dist.get('MEDIUM', 0),
            low=dist.get('LOW', 0),
            optional=dist.get('OPTIONAL', 0),
            resolved_count=resolved
        )
