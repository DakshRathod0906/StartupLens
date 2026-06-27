from ..constants import ReadinessLevel
from decimal import Decimal

class ReadinessService:
    @staticmethod
    def calculate_readiness(overall_assessment, recommendation_summary, roadmap):
        # Base Score Calculation
        # Assessment = 50%, Rec Health = 25%, Roadmap = 25%
        assessment_score = float(overall_assessment.overall_score)
        rec_health = 100.0 if not recommendation_summary.critical_count else max(0, 100 - (recommendation_summary.critical_count * 20))
        
        roadmap_completion = 0.0
        if hasattr(roadmap, 'progress') and roadmap.progress.total_tasks > 0:
            roadmap_completion = float(roadmap.progress.completion_percentage)
            
        final_score = (assessment_score * 0.5) + (rec_health * 0.25) + (roadmap_completion * 0.25)
        final_score = min(max(final_score, 0.0), 100.0)
        
        # Hard Gates
        critical_recs = recommendation_summary.critical_count
        blocked_tasks = roadmap.progress.blocked_tasks if hasattr(roadmap, 'progress') else 0
        
        if final_score >= 90 and critical_recs == 0 and blocked_tasks == 0 and roadmap_completion >= 80:
            level = ReadinessLevel.INVESTMENT_READY
        elif final_score >= 75 and critical_recs <= 2 and blocked_tasks <= 2 and roadmap_completion >= 50:
            level = ReadinessLevel.PROMISING
        elif final_score >= 50:
            level = ReadinessLevel.EARLY_STAGE
        else:
            level = ReadinessLevel.NOT_READY
            
        return Decimal(str(round(final_score, 2))), level