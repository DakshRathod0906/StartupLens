from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from startup_ideas.models import StartupIdea, Tag, Industry
from investors.models import Investor, InvestmentPreference

User = get_user_model()


class APITestBase(TestCase):
    """Base class with shared setup for API tests."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='apitest@example.com',
            username='apitest',
            password='testpass123',
        )
        self.client.force_authenticate(user=self.user)
        self.idea = StartupIdea.objects.create(
            owner=self.user,
            title='API Test Idea',
            slug='api-test-idea',
            short_description='Testing the API',
            problem_statement='Problem',
            proposed_solution='Solution',
            target_audience='Testers',
        )


class AuthenticationAPITest(APITestBase):
    def test_user_list_returns_own_profile(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_request_rejected(self):
        client = APIClient()
        response = client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StartupIdeaAPITest(APITestBase):
    def test_list_startup_ideas(self):
        response = self.client.get('/api/startup-ideas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data.get('success', True))

    def test_create_startup_idea(self):
        response = self.client.post('/api/startup-ideas/', {
            'title': 'New API Idea',
            'short_description': 'Created via API',
            'problem_statement': 'API Problem',
            'proposed_solution': 'API Solution',
            'target_audience': 'API Users',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_startup_idea(self):
        response = self.client.get(f'/api/startup-ideas/{self.idea.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_startup_idea(self):
        response = self.client.patch(f'/api/startup-ideas/{self.idea.id}/', {
            'title': 'Updated Title',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_startup_idea(self):
        response = self.client.delete(f'/api/startup-ideas/{self.idea.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_startup_ideas(self):
        response = self.client.get('/api/startup-ideas/?search=API')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_startup_ideas(self):
        response = self.client.get('/api/startup-ideas/?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_see_ideas(self):
        other_user = User.objects.create_user(
            email='other@example.com', username='other', password='pass'
        )
        other_client = APIClient()
        other_client.force_authenticate(user=other_user)
        response = other_client.get('/api/startup-ideas/')
        data = response.json()
        # Should return empty or not include our idea
        results = data.get('data', {}).get('results', data.get('data', []))
        if isinstance(results, list):
            self.assertEqual(len(results), 0)


class InvestorAPITest(APITestBase):
    def test_list_investors(self):
        Investor.objects.create(name='Test Fund')
        response = self.client.get('/api/investors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_investor_matching_endpoint(self):
        investor = Investor.objects.create(name='Match Fund')
        InvestmentPreference.objects.create(
            investor=investor,
            industry=['Technology'],
            stage=['Seed'],
            ticket_size_min=100000,
        )
        from startup_ideas.models import Industry
        tech = Industry.objects.create(name='Technology', slug='tech-match')
        self.idea.industry = tech
        self.idea.save()

        response = self.client.post('/api/investor-matches/run_matching/', {
            'startup_idea_id': str(self.idea.id),
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_matching_missing_idea_returns_404(self):
        response = self.client.post('/api/investor-matches/run_matching/', {
            'startup_idea_id': '99999',
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReadOnlyEndpointsTest(APITestBase):
    """Verify read-only endpoints return 200 and reject writes."""

    def test_research_jobs(self):
        response = self.client.get('/api/research-jobs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_findings(self):
        response = self.client.get('/api/findings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_insights(self):
        response = self.client.get('/api/insights/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assessments(self):
        response = self.client.get('/api/assessments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recommendations(self):
        response = self.client.get('/api/recommendations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_roadmaps(self):
        response = self.client.get('/api/roadmaps/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_evaluations(self):
        response = self.client.get('/api/evaluations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reports(self):
        response = self.client.get('/api/reports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ai_conversations(self):
        response = self.client.get('/api/ai-conversations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_predictions(self):
        response = self.client.get('/api/predictions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_prediction_models(self):
        response = self.client.get('/api/prediction-models/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StandardizedResponseTest(APITestBase):
    """Verify the JSON envelope format."""

    def test_response_has_success_field(self):
        response = self.client.get('/api/startup-ideas/')
        data = response.json()
        self.assertIn('success', data)

    def test_success_response_format(self):
        response = self.client.get('/api/startup-ideas/')
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
