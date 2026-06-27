from abc import ABC, abstractmethod
from typing import List, Dict, Any
from research.models import ResearchSource

class BaseExtractor(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def supports(self, source: ResearchSource) -> bool:
        """Determines if this extractor can process the given source."""
        pass

    @abstractmethod
    def extract(self, source: ResearchSource) -> List[Dict[str, Any]]:
        """
        Extracts structured findings from the source.
        Returns a list of dictionaries with keys:
        - raw_title
        - raw_description
        - raw_confidence (numeric)
        - metadata
        """
        pass
