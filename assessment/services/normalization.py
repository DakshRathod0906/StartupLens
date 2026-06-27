from decimal import Decimal

class NormalizationService:
    @staticmethod
    def normalize_to_percentage(raw_score: Decimal, max_score: Decimal) -> Decimal:
        """
        Converts a raw score to a 0-100 percentage.
        """
        if max_score <= Decimal('0.0'):
            return Decimal('0.0')
            
        percentage = (raw_score / max_score) * Decimal('100.0')
        percentage = max(Decimal('0.0'), min(percentage, Decimal('100.0')))
        
        return Decimal(str(round(percentage, 2)))
