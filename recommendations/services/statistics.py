from django.db.models import Count
from ..models import Recommendation, RecommendationStatus
from ..constants import RecommendationPriority

class StatisticsService:
    @staticmethod
    def get_priority_distribution():
        active_recs = Recommendation.objects.filter(status=RecommendationStatus.ACTIVE)
        
        counts = {
            RecommendationPriority.CRITICAL: 0,
            RecommendationPriority.HIGH: 0,
            RecommendationPriority.MEDIUM: 0,
            RecommendationPriority.LOW: 0,
            RecommendationPriority.OPTIONAL: 0
        }
        
        dist = active_recs.values('priority').annotate(count=Count('id'))
        for d in dist:
            if d['priority'] in counts:
                counts[d['priority']] = d['count']
                
        return counts
