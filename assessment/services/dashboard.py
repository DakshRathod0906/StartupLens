from dataclasses import dataclass
from decimal import Decimal
from django.db.models import Avg, Max, Min
from ..models import Assessment, OverallAssessment
from ..constants import AssessmentStatus

@dataclass
class AssessmentStatistics:
    total_assessments: int
    overall_average: Decimal
    highest_score: Decimal
    lowest_score: Decimal
    latest_assessment: str
    total_versions: int

class DashboardService:
    @staticmethod
    def get_statistics() -> AssessmentStatistics:
        active_assessments = Assessment.objects.filter(status=AssessmentStatus.GENERATED)
        
        total = active_assessments.count()
        
        avg_dict = active_assessments.aggregate(
            avg=Avg('percentage'),
            highest=Max('percentage'),
            lowest=Min('percentage')
        )
        
        avg_score = Decimal(avg_dict['avg'] or 0).quantize(Decimal('0.01'))
        highest = Decimal(avg_dict['highest'] or 0).quantize(Decimal('0.01'))
        lowest = Decimal(avg_dict['lowest'] or 0).quantize(Decimal('0.01'))
        
        latest_overall = OverallAssessment.objects.order_by('-created_at').first()
        latest_str = f"{latest_overall.overall_score}% ({latest_overall.grade})" if latest_overall else "N/A"
        
        total_versions = OverallAssessment.objects.count()
        
        return AssessmentStatistics(
            total_assessments=total,
            overall_average=avg_score,
            highest_score=highest,
            lowest_score=lowest,
            latest_assessment=latest_str,
            total_versions=total_versions
        )
