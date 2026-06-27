from typing import List, Dict, Any
from .base import BaseAggregator
from startup_ideas.models import StartupIdea
from knowledge.models import Finding
from knowledge.constants import FindingType
from ..constants import InsightType
from decimal import Decimal

class CompetitorAggregator(BaseAggregator):
    @property
    def name(self) -> str:
        return "CompetitorAggregator"

    def supports(self, finding_type: str) -> bool:
        return finding_type == FindingType.COMPETITOR

    def aggregate(self, startup_idea: StartupIdea, findings: List[Finding]) -> List[Dict[str, Any]]:
        insights = []
        if not findings:
            return insights
            
        # Mock aggregation: group by normalized_title
        grouped = {}
        for f in findings:
            key = f.normalized_title
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(f)
            
        for key, group_findings in grouped.items():
            providers = set(f.research_source.provider for f in group_findings)
            avg_conf = sum(float(f.confidence_score) for f in group_findings) / len(group_findings)
            
            insights.append({
                "title": group_findings[0].title,
                "summary": f"Competitor {group_findings[0].title} mentioned {len(group_findings)} times.",
                "insight_type": InsightType.COMPETITION,
                "confidence_score": Decimal(str(round(avg_conf, 2))),
                "metadata": {
                    "provider_count": len(providers),
                    "finding_count": len(group_findings),
                    "top_domains": list(set(f.research_source.domain for f in group_findings))
                },
                "supporting_finding_ids": [f.id for f in group_findings]
            })
            
        return insights
