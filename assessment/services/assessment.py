import logging
from django.db import transaction
from startup_ideas.models import StartupIdea
from business_intelligence.models import Insight
from business_intelligence.constants import InsightStatus
from ..models import Assessment, OverallAssessment
from ..constants import AssessmentStatus
from ..evaluators import ALL_EVALUATORS
from .weighting import WeightingService
from .scoring import ScoringService

logger = logging.getLogger(__name__)

class AssessmentService:
    @staticmethod
    def generate_assessments(idea: StartupIdea):
        """
        Coordinates the assessment generation for a startup idea.
        """
        # Load verified insights (or generated if we skip verification for now)
        # Using GENERATED as per Phase 5 status quo
        insights = list(Insight.objects.filter(startup_idea=idea, status__in=[InsightStatus.GENERATED, InsightStatus.VERIFIED]))
        
        assessments_created = []
        
        for evaluator in ALL_EVALUATORS:
            try:
                # 1. Get Rule
                rule = WeightingService.get_rule(evaluator.assessment_type)
                if not rule.is_active:
                    continue
                
                # 2. Filter Insights
                supported_insights = [i for i in insights if evaluator.supports(i.insight_type)]
                
                # 3. Get Raw Metrics
                raw_metrics = evaluator.evaluate(idea, supported_insights, rule)
                
                # 4. Score and Grade
                scored_data = ScoringService.process_raw_metrics(raw_metrics, rule)
                
                # 5. Supersede old assessments for this specific category
                Assessment.objects.filter(
                    startup_idea=idea,
                    assessment_type=evaluator.assessment_type,
                    status=AssessmentStatus.GENERATED
                ).update(status=AssessmentStatus.SUPERSEDED)
                
                # Calculate version
                last_version = Assessment.objects.filter(
                    startup_idea=idea,
                    assessment_type=evaluator.assessment_type
                ).order_by('-version').first()
                
                next_version = 1 if not last_version else last_version.version + 1
                
                with transaction.atomic():
                    assessment = Assessment.objects.create(
                        startup_idea=idea,
                        assessment_type=evaluator.assessment_type,
                        score=scored_data['score'],
                        max_score=scored_data['max_score'],
                        percentage=scored_data['percentage'],
                        grade=scored_data['grade'],
                        summary=scored_data['summary'],
                        strengths=scored_data['strengths'],
                        weaknesses=scored_data['weaknesses'],
                        status=AssessmentStatus.GENERATED,
                        version=next_version,
                        metadata={
                            "evaluated_insights": len(supported_insights),
                            "weight": float(rule.weight),
                            "formula": "weighted_average_v1"
                        }
                    )
                    
                    insight_ids = scored_data['supporting_insight_ids']
                    if insight_ids:
                        assessment.generated_from_insights.add(*insight_ids)
                        
                    assessments_created.append(assessment)
                    
            except Exception as e:
                logger.error(f"Evaluator {evaluator.assessment_type} failed for idea {idea.id}: {e}")
                
        # 6. Generate Overall Assessment
        if assessments_created:
            AssessmentService._generate_overall(idea)
            
    @staticmethod
    def _generate_overall(idea: StartupIdea):
        active_assessments = Assessment.objects.filter(
            startup_idea=idea,
            status=AssessmentStatus.GENERATED
        )
        
        overall_data = ScoringService.calculate_overall(active_assessments)
        
        last_version = OverallAssessment.objects.filter(startup_idea=idea).order_by('-version').first()
        next_version = 1 if not last_version else last_version.version + 1
        
        OverallAssessment.objects.create(
            startup_idea=idea,
            overall_score=overall_data['overall_score'],
            grade=overall_data['grade'],
            version=next_version,
            summary=f"Overall assessment based on {len(active_assessments)} categories.",
            metadata={
                "categories_evaluated": len(active_assessments)
            }
        )
