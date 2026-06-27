from django.test import TestCase
from decimal import Decimal
from ..services.normalization import NormalizationService
from ..services.classification import ClassificationService
from ..constants import FindingType

class ServiceTests(TestCase):
    def test_normalize_title(self):
        title = "Chat GPT !@#"
        normalized = NormalizationService.normalize_title(title)
        self.assertEqual(normalized, "chat gpt")
        
    def test_normalize_text(self):
        text = "  This   is some \n  text  "
        normalized = NormalizationService.normalize_text(text)
        self.assertEqual(normalized, "This is some text")

    def test_classification(self):
        finding_type = ClassificationService.classify("ChatGPT", "AI", "CompetitorExtractor")
        self.assertEqual(finding_type, FindingType.COMPETITOR)
        
        finding_type2 = ClassificationService.classify("AI Growth", "Big trend in 2026", "TrendExtractor")
        self.assertEqual(finding_type2, FindingType.MARKET_TREND)
