from decimal import Decimal
from typing import Dict
from ..models import AssessmentRule
from ..constants import AssessmentType

class WeightingService:
    @staticmethod
    def get_rule(assessment_type: str) -> AssessmentRule:
        rule, _ = AssessmentRule.objects.get_or_create(
            assessment_type=assessment_type,
            defaults={
                'weight': Decimal('10.0'),
                'minimum_score': Decimal('0.0'),
                'maximum_score': Decimal('100.0'),
                'is_active': True
            }
        )
        return rule

    @staticmethod
    def get_active_weights() -> Dict[str, Decimal]:
        rules = AssessmentRule.objects.filter(is_active=True)
        return {r.assessment_type: r.weight for r in rules}
