from django.test import TestCase
from django.contrib.auth import get_user_model
from ai.models import PromptTemplate, AIConversation, AIRequest
from ai.prompt_builder import PromptBuilder
from ai.response_parser import ResponseParser
from startup_ideas.models import StartupIdea

User = get_user_model()


class PromptTemplateTest(TestCase):
    def test_creation(self):
        template = PromptTemplate.objects.create(
            name='Test Prompt',
            version='1.0',
            system_prompt='You are a startup analyst.',
            user_prompt='Analyze {idea_title}.',
        )
        self.assertEqual(str(template), 'Test Prompt (v1.0)')
        self.assertTrue(template.is_active)

    def test_unique_constraint(self):
        PromptTemplate.objects.create(name='P', version='1.0', system_prompt='s', user_prompt='u')
        with self.assertRaises(Exception):
            PromptTemplate.objects.create(name='P', version='1.0', system_prompt='s', user_prompt='u')


class AIConversationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='t@t.com', username='t', password='p')
        self.idea = StartupIdea.objects.create(
            owner=self.user, title='I', slug='i',
            short_description='d', problem_statement='p',
            proposed_solution='s', target_audience='a',
        )

    def test_conversation_creation(self):
        conv = AIConversation.objects.create(startup_idea=self.idea, title='Test Chat')
        self.assertIn('Test Chat', str(conv))


class AIRequestTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='t@t.com', username='t', password='p')
        self.idea = StartupIdea.objects.create(
            owner=self.user, title='I', slug='i',
            short_description='d', problem_statement='p',
            proposed_solution='s', target_audience='a',
        )
        self.conv = AIConversation.objects.create(startup_idea=self.idea, title='Chat')

    def test_request_creation(self):
        req = AIRequest.objects.create(
            conversation=self.conv,
            service_name='TestService',
            model_name='gemini-2.5-flash',
            input_hash='abc123',
        )
        self.assertEqual(req.status, 'PENDING')
        self.assertEqual(req.tokens_used, 0)


class PromptBuilderTest(TestCase):
    def test_build_with_context(self):
        template = PromptTemplate.objects.create(
            name='Test', version='1.0',
            system_prompt='Analyze {idea}.',
            user_prompt='The idea is {idea}.',
        )
        system, user = PromptBuilder.build(template, {'idea': 'FoodTech'})
        self.assertIn('FoodTech', system)
        self.assertIn('FoodTech', user)

    def test_build_with_missing_key(self):
        template = PromptTemplate.objects.create(
            name='Test2', version='1.0',
            system_prompt='Analyze {missing_key}.',
            user_prompt='Done.',
        )
        system, user = PromptBuilder.build(template, {})
        # Should gracefully fallback
        self.assertIn('{missing_key}', system)


class ResponseParserTest(TestCase):
    def test_parse_json(self):
        result = ResponseParser.parse_json('{"score": 85}')
        self.assertEqual(result['score'], 85)

    def test_parse_json_with_markdown_wrapper(self):
        raw = '```json\n{"score": 85}\n```'
        result = ResponseParser.parse_json(raw)
        self.assertEqual(result['score'], 85)

    def test_parse_json_invalid(self):
        with self.assertRaises(ValueError):
            ResponseParser.parse_json('not json')

    def test_parse_markdown(self):
        result = ResponseParser.parse_markdown('  Hello  ')
        self.assertEqual(result, 'Hello')
