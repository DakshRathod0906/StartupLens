from decimal import Decimal
from ..constants import ResearchProvider

class SourceScoringService:
    @staticmethod
    def calculate_score(provider: str, domain: str) -> Decimal:
        """
        Assigns a deterministic credibility score based on domain and provider.
        Scale: 0.00 to 10.00
        """
        base_scores = {
            ResearchProvider.GITHUB: Decimal('8.50'),
            ResearchProvider.NEWS: Decimal('7.00'),
            ResearchProvider.REDDIT: Decimal('5.00'),
            ResearchProvider.WEBSITE: Decimal('4.00'),
            ResearchProvider.GOOGLE: Decimal('4.00'),
        }
        
        score = base_scores.get(provider, Decimal('4.00'))
        
        # Simple domain boosts
        high_trust_domains = ['github.com', 'techcrunch.com', 'ycombinator.com']
        if any(d in domain.lower() for d in high_trust_domains):
            score += Decimal('1.50')
            
        return min(score, Decimal('10.00'))
