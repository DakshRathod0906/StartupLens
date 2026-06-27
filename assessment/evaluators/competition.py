from typing import List, Dict, Any
from decimal import Decimal
from .base import BaseEvaluator
from startup_ideas.models import StartupIdea
from business_intelligence.models import Insight
from business_intelligence.constants import InsightType
from ..models import AssessmentRule
from ..constants import AssessmentType

class CompetitionEvaluator(BaseEvaluator):
    @property
    def assessment_type(self) -> str:
        return AssessmentType.COMPETITION

    def supports(self, insight_type: str) -> bool:
        return insight_type == InsightType.COMPETITION

    def evaluate(self, startup_idea: StartupIdea, insights: List[Insight], rule: AssessmentRule) -> Dict[str, Any]:
        if not insights:
            return {
                "raw_score": Decimal('0.0'),
                "max_score": rule.maximum_score,
                "summary": "No competition insights found.",
                "strengths": [],
                "weaknesses": ["Zero visibility into competitive landscape."],
                "supporting_insight_ids": []
            }
            
        avg_conf = sum(i.confidence_score for i in insights) / len(insights)
        
        # Penalize if too many competitors, but reward high confidence understanding
        raw_score = (Decimal('100.0') - (len(insights) * Decimal('5.0'))) * avg_conf
        raw_score = max(Decimal('0.0'), min(raw_score, rule.maximum_score))
        
        strengths = []
        weaknesses = []
        if len(insights) < 3:
            strengths.append("Low number of identified direct competitors.")
        else:
            weaknesses.append("Crowded competitive landscape.")
            
        if avg_conf > Decimal('0.7'):
            strengths.append("High confidence in competitive data.")
            
        return {
            "raw_score": raw_score,
            "max_score": rule.maximum_score,
            "summary": f"Evaluated {len(insights)} competitor insights.",
            "strengths": strengths,
            "weaknesses": weaknesses,
            "supporting_insight_ids": [i.id for i in insights]
        }
