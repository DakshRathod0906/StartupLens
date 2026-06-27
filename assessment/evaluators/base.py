from abc import ABC, abstractmethod
from typing import List, Dict, Any
from startup_ideas.models import StartupIdea
from business_intelligence.models import Insight
from ..models import AssessmentRule

class BaseEvaluator(ABC):
    @property
    @abstractmethod
    def assessment_type(self) -> str:
        pass

    @abstractmethod
    def supports(self, insight_type: str) -> bool:
        """Determines if this evaluator processes the given insight type."""
        pass

    @abstractmethod
    def evaluate(self, startup_idea: StartupIdea, insights: List[Insight], rule: AssessmentRule) -> Dict[str, Any]:
        """
        Evaluates insights and determines raw metrics.
        Returns a dictionary with raw data that the ScoringService will process.
        Expected keys:
        - raw_score
        - max_score
        - summary
        - strengths (list of str)
        - weaknesses (list of str)
        - supporting_insight_ids
        """
        pass
