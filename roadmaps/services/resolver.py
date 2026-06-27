from typing import List
from startup_ideas.models import StartupIdea
from recommendations.models import Recommendation
from recommendations.constants import RecommendationStatus

class RecommendationResolverService:
    @staticmethod
    def resolve_active(idea: StartupIdea) -> List[Recommendation]:
        """
        Loads all active recommendations for a given startup idea.
        """
        return list(Recommendation.objects.filter(
            startup_idea=idea,
            status=RecommendationStatus.ACTIVE
        ).order_by('-priority'))
