from ..constants import FindingType

class ClassificationService:
    @staticmethod
    def classify(title: str, description: str, extractor_name: str) -> str:
        if "Competitor" in extractor_name:
            return FindingType.COMPETITOR
        if "Market" in extractor_name:
            return FindingType.MARKET_SIZE
            
        text = (title + " " + description).lower()
        if "trend" in text:
            return FindingType.MARKET_TREND
        if "pricing" in text:
            return FindingType.PRICING
            
        return FindingType.OTHER
