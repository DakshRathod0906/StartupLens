from decimal import Decimal
from research.models import ResearchSource

class ConfidenceService:
    @staticmethod
    def calculate_confidence(source: ResearchSource, raw_confidence: float) -> Decimal:
        """
        Combines source credibility score (0-10) with extractor's raw confidence (0-1).
        Returns a deterministic threshold value.
        """
        source_factor = float(source.credibility_score) / 10.0
        final = (source_factor * 0.4) + (raw_confidence * 0.6)
        
        if final >= 0.85:
            return Decimal('0.95')
        elif final >= 0.5:
            return Decimal('0.50')
        else:
            return Decimal('0.25')
