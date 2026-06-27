from django.test import TestCase
from decimal import Decimal
from ..services.normalization import NormalizationService
from ..services.source_scoring import SourceScoringService
from ..constants import ResearchProvider

class ServiceTests(TestCase):
    def test_canonicalize_url(self):
        url = "https://example.com/article?utm_source=google&fbclid=123&keep=this"
        canonical = NormalizationService.canonicalize_url(url)
        self.assertEqual(canonical, "https://example.com/article?keep=this")
        
        url2 = "https://example.com/path/#fragment"
        canonical2 = NormalizationService.canonicalize_url(url2)
        self.assertEqual(canonical2, "https://example.com/path/")

    def test_content_hash(self):
        text1 = "  This   is some \n  text  "
        text2 = "This is some text"
        self.assertEqual(
            NormalizationService.generate_content_hash(text1),
            NormalizationService.generate_content_hash(text2)
        )

    def test_source_scoring(self):
        score = SourceScoringService.calculate_score(ResearchProvider.GITHUB, "github.com/repo")
        self.assertEqual(score, Decimal('10.00')) # 8.50 + 1.50 = 10.00
        
        score2 = SourceScoringService.calculate_score(ResearchProvider.GOOGLE, "random.com")
        self.assertEqual(score2, Decimal('4.00'))
