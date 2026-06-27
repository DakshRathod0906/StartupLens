from django.test import TestCase
from django.contrib.auth import get_user_model
from reports.models import ReportTemplate, ReportSection, Report
from evaluation.models import FinalEvaluation, EvaluationSnapshot
from assessment.models import OverallAssessment
from recommendations.models import RecommendationSummary
from roadmaps.models import Roadmap
from startup_ideas.models import StartupIdea

User = get_user_model()


class ReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', username='testuser', password='testpass123'
        )
        self.idea = StartupIdea.objects.create(
            owner=self.user,
            title='Test Idea',
            slug='test-idea',
            short_description='A test startup idea',
            problem_statement='Test problem',
            proposed_solution='Test solution',
            target_audience='Test audience',
        )

    def test_report_template_creation(self):
        template = ReportTemplate.objects.create(name='Test Template', version='1.0')
        self.assertEqual(str(template), 'Test Template (v1.0)')
        self.assertTrue(template.is_active)

    def test_report_template_unique_constraint(self):
        ReportTemplate.objects.create(name='Test Template', version='1.0')
        with self.assertRaises(Exception):
            ReportTemplate.objects.create(name='Test Template', version='1.0')

    def test_report_section_ordering(self):
        template = ReportTemplate.objects.create(name='T', version='1.0')
        s1 = ReportSection.objects.create(template=template, title='Second', order=2, content_type='text')
        s2 = ReportSection.objects.create(template=template, title='First', order=1, content_type='text')
        sections = list(template.sections.all())
        self.assertEqual(sections[0].title, 'First')
        self.assertEqual(sections[1].title, 'Second')

    def test_report_status_choices(self):
        self.assertEqual(Report.StatusChoices.PENDING, 'PENDING')
        self.assertEqual(Report.StatusChoices.COMPLETED, 'COMPLETED')
        self.assertEqual(Report.StatusChoices.FAILED, 'FAILED')
