from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User
from startup_ideas.models import StartupIdea, Industry, Tag
from common.services.slug_service import SlugService

class StartupIdeaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@test.com", password="password")
        self.industry = Industry.objects.create(name="Tech", slug="tech")

    def test_idea_creation(self):
        idea = StartupIdea.objects.create(
            owner=self.user,
            title="Test Idea",
            slug=SlugService.generate_slug("Test Idea", StartupIdea),
            short_description="Short desc",
            problem_statement="Problem",
            proposed_solution="Solution",
            target_audience="Audience",
            industry=self.industry
        )
        self.assertEqual(idea.title, "Test Idea")
        self.assertEqual(idea.slug, "test-idea")

    def test_slug_collision(self):
        idea1 = StartupIdea.objects.create(
            owner=self.user,
            title="Cool Idea",
            slug=SlugService.generate_slug("Cool Idea", StartupIdea),
            short_description="Short desc 1"
        )
        idea2 = StartupIdea.objects.create(
            owner=self.user,
            title="Cool Idea",
            slug=SlugService.generate_slug("Cool Idea", StartupIdea),
            short_description="Short desc 2"
        )
        self.assertEqual(idea1.slug, "cool-idea")
        self.assertEqual(idea2.slug, "cool-idea-2")

class StartupIdeaViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@test.com", password="password")
        self.client.force_login(self.user)
        self.industry = Industry.objects.create(name="Tech", slug="tech")
        self.idea = StartupIdea.objects.create(
            owner=self.user,
            title="Existing Idea",
            slug=SlugService.generate_slug("Existing Idea", StartupIdea),
            short_description="Desc",
            industry=self.industry
        )

    def test_dashboard_loads(self):
        response = self.client.get(reverse('startup_ideas:dashboard'))
        self.assertEqual(response.status_code, 200)
        
    def test_list_loads(self):
        response = self.client.get(reverse('startup_ideas:list'))
        self.assertEqual(response.status_code, 200)
        
    def test_create_loads(self):
        response = self.client.get(reverse('startup_ideas:create'))
        self.assertEqual(response.status_code, 200)
        
    def test_detail_loads(self):
        response = self.client.get(reverse('startup_ideas:detail', kwargs={'slug': self.idea.slug}))
        self.assertEqual(response.status_code, 200)
        
    def test_edit_loads(self):
        response = self.client.get(reverse('startup_ideas:edit', kwargs={'slug': self.idea.slug}))
        self.assertEqual(response.status_code, 200)
        
    def test_archive_loads(self):
        response = self.client.get(reverse('startup_ideas:archive', kwargs={'slug': self.idea.slug}))
        self.assertEqual(response.status_code, 200)
        
    def test_delete_loads(self):
        response = self.client.get(reverse('startup_ideas:delete', kwargs={'slug': self.idea.slug}))
        self.assertEqual(response.status_code, 200)
