from typing import Dict, Any
from decimal import Decimal
from .weighting import WeightingService
from .grading import GradeService
from .normalization import NormalizationService
from ..models import AssessmentRule

class ScoringService:
    @staticmethod
    def process_raw_metrics(raw_data: Dict[str, Any], rule: AssessmentRule) -> Dict[str, Any]:
        """
        Takes raw data from an evaluator and applies scoring rules.
        Ensures score is within [rule.minimum_score, rule.maximum_score].
        Calculates percentage and determines grade.
        """
        raw_score = raw_data.get('raw_score', Decimal('0.0'))
        max_score = raw_data.get('max_score', rule.maximum_score)
        
        # Enforce rule bounds
        score = max(rule.minimum_score, min(raw_score, rule.maximum_score))
        
        # Normalize to percentage
        percentage = NormalizationService.normalize_to_percentage(score, max_score)
        
        # Get Grade
        grade = GradeService.get_grade(percentage)
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': percentage,
            'grade': grade,
            'summary': raw_data.get('summary', ''),
            'strengths': raw_data.get('strengths', []),
            'weaknesses': raw_data.get('weaknesses', []),
            'supporting_insight_ids': raw_data.get('supporting_insight_ids', [])
        }

    @staticmethod
    def calculate_overall(assessments: list) -> Dict[str, Any]:
        """
        Calculates overall score based on the latest generated assessments and their weights.
        """
        active_weights = WeightingService.get_active_weights()
        
        total_weight = Decimal('0.0')
        weighted_sum = Decimal('0.0')
        
        for assessment in assessments:
            weight = active_weights.get(assessment.assessment_type, Decimal('0.0'))
            weighted_sum += assessment.percentage * weight
            total_weight += weight
            
        if total_weight > Decimal('0.0'):
            overall_score = weighted_sum / total_weight
        else:
            overall_score = Decimal('0.0')
            
        overall_score = Decimal(str(round(overall_score, 2)))
        grade = GradeService.get_grade(overall_score)
        
        return {
            'overall_score': overall_score,
            'grade': grade
        }
