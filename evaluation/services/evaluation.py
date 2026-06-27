from django.db import transaction
from .readiness import ReadinessService
from .confidence import ConfidenceService
from .strengths import StrengthService
from .risks import RiskService
from .summary import SummaryService
from ..models import FinalEvaluation, EvaluationSnapshot
from ..constants import EvaluationStatus

class EvaluationService:
    @staticmethod
    @transaction.atomic
    def generate_evaluation(startup_idea, overall_assessment, recommendation_summary, roadmap):
        # 1. Supersede old evaluations
        FinalEvaluation.objects.filter(
            startup_idea=startup_idea,
            status=EvaluationStatus.GENERATED
        ).update(status=EvaluationStatus.ARCHIVED)
        
        # 2. Calculate metrics
        if overall_assessment and recommendation_summary:
            readiness_score, readiness_level = ReadinessService.calculate_readiness(overall_assessment, recommendation_summary, roadmap)
            confidence_score = ConfidenceService.calculate_confidence(overall_assessment, recommendation_summary, roadmap)
            strengths = StrengthService.extract_strengths(overall_assessment, recommendation_summary)
            risks = RiskService.extract_risks(overall_assessment, recommendation_summary, roadmap)
            executive_summary = SummaryService.generate_summary(readiness_level, strengths, risks)
        else:
            readiness_score, readiness_level = 0.0, "NOT_READY"
            confidence_score = 0.0
            strengths = []
            risks = ["Insufficient data generated from previous steps."]
            executive_summary = "Evaluation cannot be completed due to missing assessment or recommendation data."
        
        # 3. Next version
        last_eval = FinalEvaluation.objects.filter(startup_idea=startup_idea).order_by('-version').first()
        next_version = last_eval.version + 1 if last_eval else 1
        
        # 4. Create new FinalEvaluation
        eval_obj = FinalEvaluation.objects.create(
            startup_idea=startup_idea,
            generated_from_overall_assessment=overall_assessment,
            overall_assessment=overall_assessment,
            recommendation_summary=recommendation_summary,
            roadmap=roadmap,
            readiness_score=readiness_score,
            readiness_level=readiness_level,
            overall_grade=overall_assessment.grade if overall_assessment else "N/A",
            executive_summary=executive_summary,
            key_strengths=strengths,
            key_risks=risks,
            critical_actions=[], # Simplified for now
            confidence_score=confidence_score,
            version=next_version,
            status=EvaluationStatus.GENERATED
        )
        
        # 5. Create Snapshot
        EvaluationSnapshot.objects.create(
            final_evaluation=eval_obj,
            assessment_snapshot={"score": str(overall_assessment.overall_score) if overall_assessment else "N/A"},
            recommendation_snapshot={"critical_count": recommendation_summary.critical_count if recommendation_summary else 0},
            roadmap_snapshot={"tasks": roadmap.tasks.count() if roadmap else 0},
            strength_snapshot={"strengths": strengths},
            risk_snapshot={"risks": risks},
            summary_snapshot={"summary": executive_summary},
            overall_score_snapshot=overall_assessment.overall_score if overall_assessment else 0.0,
            overall_grade_snapshot=overall_assessment.grade if overall_assessment else "N/A"
        )
        
        return eval_obj