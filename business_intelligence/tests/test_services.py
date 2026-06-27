from django.test import TestCase
from decimal import Decimal
from ..services.normalization import NormalizationService

class ServiceTests(TestCase):
    def test_normalize_name(self):
        title = "chat GPT !@#"
        normalized = NormalizationService.normalize_name(title)
        self.assertEqual(normalized, "Chat Gpt")
