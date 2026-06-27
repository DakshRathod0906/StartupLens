from abc import ABC, abstractmethod
from typing import List, Dict, Any
from startup_ideas.models import StartupIdea
from knowledge.models import Finding

class BaseAggregator(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def supports(self, finding_type: str) -> bool:
        """Determines if this aggregator processes the given finding type."""
        pass

    @abstractmethod
    def aggregate(self, startup_idea: StartupIdea, findings: List[Finding]) -> List[Dict[str, Any]]:
        """
        Aggregates a list of findings into structured insights.
        Returns a list of dictionaries with keys:
        - title
        - summary
        - insight_type
        - confidence_score
        - metadata
        - supporting_finding_ids
        """
        pass
