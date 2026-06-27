from typing import List, Tuple
from recommendations.models import Recommendation
from ..models import RoadmapTask, TaskTemplate

class TaskGenerationService:
    @staticmethod
    def generate_prototypes(recommendations: List[Recommendation]) -> List[Tuple[Recommendation, TaskTemplate]]:
        """
        Maps active recommendations to their corresponding TaskTemplates.
        Returns a list of tuples (recommendation, template) to be used for DAG processing.
        """
        prototypes = []
        for rec in recommendations:
            try:
                template = TaskTemplate.objects.get(recommendation_rule=rec.matched_rule, is_active=True)
                prototypes.append((rec, template))
            except TaskTemplate.DoesNotExist:
                # If a recommendation rule has no active template, it cannot be scheduled.
                pass
                
        return prototypes
