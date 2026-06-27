from django.test import TestCase
from django.contrib.auth import get_user_model
from investors.models import Investor, InvestmentPreference, StartupInvestorMatch, MatchExplanation
from startup_ideas.models import StartupIdea, Industry

User = get_user_model()


class InvestorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', username='testuser', password='testpass123'
        )
        self.idea = StartupIdea.objects.create(
            owner=self.user,
            title='Test Idea',
            slug='test-idea',
            short_description='A test idea',
            problem_statement='Problem',
            proposed_solution='Solution',
            target_audience='Developers',
        )
        self.investor = Investor.objects.create(
            name='Test VC',
            description='A test VC firm',
            website='https://testvc.com',
        )

    def test_investor_creation(self):
        self.assertEqual(str(self.investor), 'Test VC')
        self.assertTrue(self.investor.is_active)

    def test_investment_preference_creation(self):
        pref = InvestmentPreference.objects.create(
            investor=self.investor,
            industry=['Technology', 'Healthcare'],
            stage=['Seed', 'Series A'],
            country=['US', 'UK'],
            ticket_size_min=50000,
            ticket_size_max=500000,
            risk_appetite='HIGH',
        )
        self.assertEqual(str(pref), 'Preferences for Test VC')
        self.assertIn('Technology', pref.industry)

    def test_match_creation(self):
        match = StartupInvestorMatch.objects.create(
            startup_idea=self.idea,
            investor=self.investor,
            compatibility_score=85,
        )
        self.assertEqual(match.match_status, 'SUGGESTED')
        self.assertIn('Test Idea', str(match))

    def test_match_explanation(self):
        match = StartupInvestorMatch.objects.create(
            startup_idea=self.idea,
            investor=self.investor,
            compatibility_score=85,
        )
        explanation = MatchExplanation.objects.create(
            match=match,
            matched_industries=['Technology'],
            matched_stage=True,
            matched_budget=True,
            reasoning='Strong industry and stage alignment.',
        )
        self.assertTrue(explanation.matched_stage)


class InvestorMatchingServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', username='testuser', password='testpass123'
        )
        self.industry = Industry.objects.create(name='Technology', slug='technology')
        self.idea = StartupIdea.objects.create(
            owner=self.user,
            title='Test Idea',
            slug='test-idea',
            short_description='A technology startup',
            problem_statement='Problem',
            proposed_solution='Solution',
            target_audience='Developers',
            industry=self.industry,
        )
        self.investor = Investor.objects.create(name='Tech Fund')
        InvestmentPreference.objects.create(
            investor=self.investor,
            industry=['Technology'],
            stage=['Seed'],
            ticket_size_min=100000,
            ticket_size_max=500000,
        )

    def test_matching_returns_results(self):
        from investors.services.matching import InvestorMatchingService
        matches = InvestorMatchingService.match_startup(self.idea)
        self.assertTrue(len(matches) > 0)
        self.assertGreater(matches[0].compatibility_score, 50)
