from decimal import Decimal
from typing import List
from knowledge.models import Finding

class ConfidenceService:
    @staticmethod
    def calculate_confidence(findings: List[Finding]) -> Decimal:
        """
        Calculates a deterministic confidence score based on:
        - Number of supporting findings
        - Average finding confidence
        """
        if not findings:
            return Decimal('0.00')
            
        avg_conf = sum(float(f.confidence_score) for f in findings) / len(findings)
        
        # Boost for having multiple findings backing this insight
        count_boost = min(len(findings) * 0.05, 0.20)
        
        final = avg_conf + count_boost
        final = min(final, 1.0)
        
        return Decimal(str(round(final, 2)))
