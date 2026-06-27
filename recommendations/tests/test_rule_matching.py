from django.test import TestCase
from decimal import Decimal
from ..services.rule_matching import RuleMatchingService
from ..models import RecommendationRule
from ..constants import RuleOperator, RecommendationPriority, RuleGroupChoices

class RuleMatchingTests(TestCase):
    def setUp(self):
        self.rule = RecommendationRule.objects.create(
            metric="market_percentage",
            operator=RuleOperator.LT,
            minimum_value=Decimal('40.0'),
            priority=RecommendationPriority.HIGH,
            rule_group=RuleGroupChoices.GROWTH,
            title="Test Rule",
            description="Test Desc",
            recommended_action="Test Action"
        )
        
    def test_lt_operator(self):
        self.assertTrue(RuleMatchingService._evaluate_operator(Decimal('39.9'), self.rule))
        self.assertFalse(RuleMatchingService._evaluate_operator(Decimal('40.0'), self.rule))
        
    def test_between_operator(self):
        self.rule.operator = RuleOperator.BETWEEN
        self.rule.minimum_value = Decimal('40.0')
        self.rule.maximum_value = Decimal('60.0')
        self.rule.save()
        
        self.assertTrue(RuleMatchingService._evaluate_operator(Decimal('50.0'), self.rule))
        self.assertTrue(RuleMatchingService._evaluate_operator(Decimal('40.0'), self.rule))
        self.assertTrue(RuleMatchingService._evaluate_operator(Decimal('60.0'), self.rule))
        self.assertFalse(RuleMatchingService._evaluate_operator(Decimal('39.9'), self.rule))
        self.assertFalse(RuleMatchingService._evaluate_operator(Decimal('60.1'), self.rule))
        
    def test_eq_operator(self):
        self.rule.operator = RuleOperator.EQ
        self.rule.minimum_value = Decimal('50.0')
        self.rule.save()
        
        self.assertTrue(RuleMatchingService._evaluate_operator(Decimal('50.0'), self.rule))
        self.assertFalse(RuleMatchingService._evaluate_operator(Decimal('50.1'), self.rule))
