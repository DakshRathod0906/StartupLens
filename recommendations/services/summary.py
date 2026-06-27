from decimal import Decimal
from typing import Optional
from django.db.models import Count
from startup_ideas.models import StartupIdea
from assessment.models import OverallAssessment
from ..models import Recommendation, RecommendationSummary
from ..constants import RecommendationStatus, RecommendationPriority

class SummaryService:
    @staticmethod
    def generate_summary(idea: StartupIdea) -> Optional[RecommendationSummary]:
        active_recommendations = Recommendation.objects.filter(
            startup_idea=idea,
            status=RecommendationStatus.ACTIVE
        )
        
        if not active_recommendations.exists():
            return None
            
        overall_assessment = OverallAssessment.objects.filter(startup_idea=idea).order_by('-version').first()
        
        # Count by priority
        counts = {
            RecommendationPriority.CRITICAL: 0,
            RecommendationPriority.HIGH: 0,
            RecommendationPriority.MEDIUM: 0,
            RecommendationPriority.LOW: 0,
            RecommendationPriority.OPTIONAL: 0
        }
        
        for rec in active_recommendations:
            counts[rec.priority] += 1
            
        total = active_recommendations.count()
        
        # Determine overall priority
        overall_priority = RecommendationPriority.OPTIONAL
        if counts[RecommendationPriority.CRITICAL] > 0:
            overall_priority = RecommendationPriority.CRITICAL
        elif counts[RecommendationPriority.HIGH] > 0:
            overall_priority = RecommendationPriority.HIGH
        elif counts[RecommendationPriority.MEDIUM] > 0:
            overall_priority = RecommendationPriority.MEDIUM
        elif counts[RecommendationPriority.LOW] > 0:
            overall_priority = RecommendationPriority.LOW
            
        executive_summary = f"Generated {total} active recommendations. Overall priority is {overall_priority}."
        
        # Versioning
        last_summary = RecommendationSummary.objects.filter(startup_idea=idea).order_by('-version').first()
        next_version = 1 if not last_summary else last_summary.version + 1
        
        summary = RecommendationSummary.objects.create(
            startup_idea=idea,
            overall_assessment=overall_assessment,
            overall_priority=overall_priority,
            executive_summary=executive_summary,
            total_recommendations=total,
            critical_count=counts[RecommendationPriority.CRITICAL],
            high_count=counts[RecommendationPriority.HIGH],
            medium_count=counts[RecommendationPriority.MEDIUM],
            low_count=counts[RecommendationPriority.LOW],
            optional_count=counts[RecommendationPriority.OPTIONAL],
            version=next_version,
            overall_score_snapshot=overall_assessment.overall_score if overall_assessment else None,
            overall_grade_snapshot=overall_assessment.grade if overall_assessment else None,
            assessment_version=overall_assessment.version if overall_assessment else None
        )
        
        return summary
