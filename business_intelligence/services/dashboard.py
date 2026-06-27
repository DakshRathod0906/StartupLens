from dataclasses import dataclass
from decimal import Decimal
from django.db.models import Avg
from ..models import Insight
from ..constants import InsightType, InsightStatus

@dataclass
class BusinessStatistics:
    total_insights: int
    competition: int
    market: int
    pricing: int
    technology: int
    risks: int
    opportunities: int
    average_confidence: Decimal
    stale_insights: int

class DashboardService:
    @staticmethod
    def get_statistics() -> BusinessStatistics:
        insights = Insight.objects.filter(status=InsightStatus.GENERATED)
        
        total = insights.count()
        competition = insights.filter(insight_type=InsightType.COMPETITION).count()
        market = insights.filter(insight_type=InsightType.MARKET).count()
        pricing = insights.filter(insight_type=InsightType.PRICING).count()
        technology = insights.filter(insight_type=InsightType.TECHNOLOGY).count()
        risks = insights.filter(insight_type=InsightType.RISK).count()
        opportunities = insights.filter(insight_type=InsightType.OPPORTUNITY).count()
        
        avg_dict = insights.aggregate(avg=Avg('confidence_score'))
        avg_score = Decimal(avg_dict['avg'] or 0).quantize(Decimal('0.01'))
        
        stale_count = Insight.objects.filter(status=InsightStatus.STALE).count()
        
        return BusinessStatistics(
            total_insights=total,
            competition=competition,
            market=market,
            pricing=pricing,
            technology=technology,
            risks=risks,
            opportunities=opportunities,
            average_confidence=avg_score,
            stale_insights=stale_count
        )
