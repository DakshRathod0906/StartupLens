from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict, Optional, Any
from assessment.models import Assessment, OverallAssessment
from startup_ideas.models import StartupIdea
from ..models import RecommendationRule
from ..constants import RuleOperator

@dataclass
class MatchedRule:
    rule: RecommendationRule
    metric: str
    actual_value: Decimal
    priority: str

class RuleMatchingService:
    @staticmethod
    def _build_metric_map(idea: StartupIdea) -> Dict[str, Any]:
        """
        Builds a map of all available metrics for a given startup idea.
        """
        metrics = {}
        
        # Load latest overall assessment
        overall = OverallAssessment.objects.filter(startup_idea=idea).order_by('-version').first()
        if overall:
            metrics['overall_score'] = overall.overall_score
            metrics['overall_grade'] = overall.grade
            
        # Load active category assessments
        active_assessments = Assessment.objects.filter(
            startup_idea=idea,
            status='GENERATED'
        )
        
        for assessment in active_assessments:
            # e.g. "MARKET" -> "market_percentage"
            metric_key = f"{assessment.assessment_type.lower()}_percentage"
            metrics[metric_key] = assessment.percentage
            
        return metrics

    @staticmethod
    def _evaluate_operator(value: Any, rule: RecommendationRule) -> bool:
        if value is None:
            return False
            
        # If the metric is a grade (string), handle equality
        if isinstance(value, str):
            if rule.operator == RuleOperator.EQ:
                # Grade rules might store "B" in minimum_value or just assume equality if properly structured.
                # Since minimum_value is Decimal, we might need a workaround for string grades, but based on the schema, 
                # we'd better convert grades to a numeric scale if they are used, or limit grade comparisons.
                pass 
            return False
            
        # Numeric comparisons
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
            
        if rule.operator == RuleOperator.LT:
            return rule.minimum_value is not None and value < rule.minimum_value
        elif rule.operator == RuleOperator.LTE:
            return rule.minimum_value is not None and value <= rule.minimum_value
        elif rule.operator == RuleOperator.GT:
            return rule.minimum_value is not None and value > rule.minimum_value
        elif rule.operator == RuleOperator.GTE:
            return rule.minimum_value is not None and value >= rule.minimum_value
        elif rule.operator == RuleOperator.EQ:
            return rule.minimum_value is not None and value == rule.minimum_value
        elif rule.operator == RuleOperator.BETWEEN:
            return (rule.minimum_value is not None and rule.maximum_value is not None and
                   rule.minimum_value <= value <= rule.maximum_value)
                   
        return False

    @staticmethod
    def match_rules(idea: StartupIdea) -> List[MatchedRule]:
        """
        Loads all active rules and evaluates them against the startup's metrics in memory.
        """
        metrics = RuleMatchingService._build_metric_map(idea)
        active_rules = RecommendationRule.objects.filter(is_active=True).order_by('display_order')
        
        matched_rules = []
        
        for rule in active_rules:
            if rule.metric in metrics:
                actual_value = metrics[rule.metric]
                
                # Evaluate rule
                if RuleMatchingService._evaluate_operator(actual_value, rule):
                    matched_rules.append(
                        MatchedRule(
                            rule=rule,
                            metric=rule.metric,
                            actual_value=actual_value,
                            priority=rule.priority
                        )
                    )
                    
        return matched_rules
