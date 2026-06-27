import logging
from django.db import transaction
from startup_ideas.models import StartupIdea
from assessment.models import OverallAssessment, Assessment
from ..models import Recommendation, RecommendationRule
from ..constants import RecommendationStatus, RecommendationCategory
from .rule_matching import RuleMatchingService
from .priority import PriorityService
from .summary import SummaryService

logger = logging.getLogger(__name__)

class RecommendationService:
    @staticmethod
    def _map_metric_to_category(metric: str) -> str:
        """
        Maps a metric like 'market_percentage' to RecommendationCategory.MARKET
        """
        if metric == 'market_percentage':
            return RecommendationCategory.MARKET
        if metric == 'competition_percentage':
            return RecommendationCategory.COMPETITION
        if metric == 'technology_percentage':
            return RecommendationCategory.TECHNOLOGY
        if metric == 'risk_percentage':
            return RecommendationCategory.RISK
        if metric == 'execution_percentage':
            return RecommendationCategory.EXECUTION
        if metric == 'funding_percentage':
            return RecommendationCategory.FUNDING
        return RecommendationCategory.OVERALL

    @staticmethod
    def generate_recommendations(idea: StartupIdea):
        """
        Coordinates the entire recommendation pipeline.
        """
        try:
            # Match rules
            matched_rules = RuleMatchingService.match_rules(idea)
            
            if not matched_rules:
                return
                
            overall_assessment = OverallAssessment.objects.filter(startup_idea=idea).order_by('-version').first()
            
            recommendations_created = []
            
            for match in matched_rules:
                # 1. Priority Calculation
                final_priority = PriorityService.calculate_final_priority(match.priority, overall_assessment)
                
                # 2. Supersede old recommendations specifically for this rule and startup
                Recommendation.objects.filter(
                    startup_idea=idea,
                    matched_rule=match.rule,
                    status__in=[RecommendationStatus.GENERATED, RecommendationStatus.ACTIVE]
                ).update(status=RecommendationStatus.SUPERSEDED)
                
                # 3. Versioning
                last_version = Recommendation.objects.filter(
                    startup_idea=idea,
                    matched_rule=match.rule
                ).order_by('-version').first()
                
                next_version = 1 if not last_version else last_version.version + 1
                
                # Try to map back to a specific assessment if applicable
                assessment = None
                category = RecommendationService._map_metric_to_category(match.metric)
                if category != RecommendationCategory.OVERALL:
                    assessment = Assessment.objects.filter(
                        startup_idea=idea, 
                        assessment_type=category,
                        status='GENERATED'
                    ).first()
                
                with transaction.atomic():
                    rec = Recommendation.objects.create(
                        startup_idea=idea,
                        assessment=assessment,
                        matched_rule=match.rule,
                        priority=final_priority,
                        category=category,
                        status=RecommendationStatus.ACTIVE,
                        title=match.rule.title,
                        description=match.rule.description,
                        recommended_action=match.rule.recommended_action,
                        version=next_version,
                        metadata={
                            "actual_value": float(match.actual_value),
                            "metric": match.metric,
                            "original_priority": match.rule.priority,
                            "adjusted_priority": final_priority
                        }
                    )
                    recommendations_created.append(rec)
            
            # 4. Generate Summary
            if recommendations_created:
                SummaryService.generate_summary(idea)
                
        except Exception as e:
            logger.error(f"Error generating recommendations for idea {idea.id}: {e}")
