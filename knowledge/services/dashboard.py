from dataclasses import dataclass
from decimal import Decimal
from django.db.models import Avg
from ..models import Finding
from ..constants import FindingType, ProcessingStatus

@dataclass
class KnowledgeStatistics:
    total_findings: int
    competitors: int
    market_trends: int
    risks: int
    opportunities: int
    average_confidence: Decimal

class DashboardService:
    @staticmethod
    def get_statistics() -> KnowledgeStatistics:
        findings = Finding.objects.filter(processing_status=ProcessingStatus.EXTRACTED)
        
        total = findings.count()
        competitors = findings.filter(finding_type=FindingType.COMPETITOR).count()
        market_trends = findings.filter(finding_type=FindingType.MARKET_TREND).count()
        risks = findings.filter(finding_type=FindingType.RISK).count()
        opportunities = findings.filter(finding_type=FindingType.OPPORTUNITY).count()
        
        avg_dict = findings.aggregate(avg=Avg('confidence_score'))
        avg_score = Decimal(avg_dict['avg'] or 0).quantize(Decimal('0.01'))
        
        return KnowledgeStatistics(
            total_findings=total,
            competitors=competitors,
            market_trends=market_trends,
            risks=risks,
            opportunities=opportunities,
            average_confidence=avg_score
        )
