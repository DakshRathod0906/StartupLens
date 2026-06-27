from decimal import Decimal
from typing import Optional
from assessment.models import OverallAssessment
from ..constants import RecommendationPriority

class PriorityService:
    @staticmethod
    def calculate_final_priority(base_priority: str, overall_assessment: Optional[OverallAssessment]) -> str:
        """
        Adjusts the base priority of a matched rule based on the startup's overall health.
        For example, a HIGH severity competition risk might be downgraded to MEDIUM if the 
        overall health of the startup is exceptional (e.g. > 90%).
        """
        if not overall_assessment:
            return base_priority
            
        # Example logic: Downgrade priority if overall health is A+ (>90%)
        # and base priority is CRITICAL or HIGH.
        if overall_assessment.overall_score >= Decimal('90.0'):
            if base_priority == RecommendationPriority.CRITICAL:
                return RecommendationPriority.HIGH
            elif base_priority == RecommendationPriority.HIGH:
                return RecommendationPriority.MEDIUM
                
        return base_priority

    @staticmethod
    def get_priority_weight(priority: str) -> int:
        """Helper for sorting priorities."""
        weights = {
            RecommendationPriority.CRITICAL: 5,
            RecommendationPriority.HIGH: 4,
            RecommendationPriority.MEDIUM: 3,
            RecommendationPriority.LOW: 2,
            RecommendationPriority.OPTIONAL: 1
        }
        return weights.get(priority, 0)
