from django.test import TestCase
from decimal import Decimal
from ..services.grading import GradeService
from ..services.normalization import NormalizationService
from ..services.scoring import ScoringService
from ..models import AssessmentRule
from ..constants import AssessmentType

class ServiceTests(TestCase):
    def test_grade_service(self):
        self.assertEqual(GradeService.get_grade(Decimal('95.0')), "A+")
        self.assertEqual(GradeService.get_grade(Decimal('85.0')), "A")
        self.assertEqual(GradeService.get_grade(Decimal('75.0')), "B")
        self.assertEqual(GradeService.get_grade(Decimal('65.0')), "C")
        self.assertEqual(GradeService.get_grade(Decimal('55.0')), "D")
        self.assertEqual(GradeService.get_grade(Decimal('45.0')), "F")

    def test_normalization_service(self):
        pct = NormalizationService.normalize_to_percentage(Decimal('7.5'), Decimal('10.0'))
        self.assertEqual(pct, Decimal('75.00'))

    def test_scoring_service(self):
        rule = AssessmentRule(
            assessment_type=AssessmentType.MARKET,
            weight=Decimal('10.0'),
            minimum_score=Decimal('0.0'),
            maximum_score=Decimal('10.0')
        )
        
        raw_data = {
            'raw_score': Decimal('8.5'),
            'max_score': Decimal('10.0'),
            'summary': "Good market.",
            'strengths': ["Large TAM"],
            'weaknesses': []
        }
        
        scored = ScoringService.process_raw_metrics(raw_data, rule)
        self.assertEqual(scored['score'], Decimal('8.5'))
        self.assertEqual(scored['percentage'], Decimal('85.00'))
        self.assertEqual(scored['grade'], "A")
