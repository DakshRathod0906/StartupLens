from django.test import TestCase
from django.contrib.auth import get_user_model
from ml.models import PredictionModel, PredictionResult, StartupFeatureVector, TrainingRun
from startup_ideas.models import StartupIdea

User = get_user_model()


class PredictionModelTest(TestCase):
    def test_creation(self):
        model = PredictionModel.objects.create(
            name='StartupPredictor',
            algorithm='XGBoost',
            version='1.0',
            feature_schema_version='1.0',
            accuracy=0.85,
            precision=0.83,
            recall=0.87,
            f1_score=0.85,
            artifact_path='models/xgboost_v1.joblib',
            is_active=True,
        )
        self.assertIn('XGBoost', str(model))
        self.assertTrue(model.is_active)

    def test_unique_constraint(self):
        PredictionModel.objects.create(
            name='M', algorithm='RF', version='1.0',
            feature_schema_version='1.0', artifact_path='x',
        )
        with self.assertRaises(Exception):
            PredictionModel.objects.create(
                name='M', algorithm='RF', version='1.0',
                feature_schema_version='1.0', artifact_path='x',
            )


class StartupFeatureVectorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='t@t.com', username='t', password='p')
        self.idea = StartupIdea.objects.create(
            owner=self.user, title='I', slug='i',
            short_description='d', problem_statement='p',
            proposed_solution='s', target_audience='a',
        )

    def test_feature_vector_creation(self):
        vector = StartupFeatureVector.objects.create(
            startup_idea=self.idea,
            schema_version='1.0',
            features={'market_size': 0.8, 'team_experience': 0.6},
        )
        self.assertEqual(vector.features['market_size'], 0.8)


class PredictionResultTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='t@t.com', username='t', password='p')
        self.idea = StartupIdea.objects.create(
            owner=self.user, title='I', slug='i',
            short_description='d', problem_statement='p',
            proposed_solution='s', target_audience='a',
        )
        self.model = PredictionModel.objects.create(
            name='M', algorithm='XGBoost', version='1.0',
            feature_schema_version='1.0', artifact_path='x', is_active=True,
        )

    def test_prediction_result_creation(self):
        result = PredictionResult.objects.create(
            startup_idea=self.idea,
            model=self.model,
            predicted_success_probability=0.75,
            predicted_failure_probability=0.25,
            feature_importances={'market': 0.4},
        )
        self.assertEqual(result.predicted_success_probability, 0.75)
        self.assertIn('I', str(result))


class PredictionServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='t@t.com', username='t', password='p')
        self.idea = StartupIdea.objects.create(
            owner=self.user, title='I', slug='i',
            short_description='d', problem_statement='p',
            proposed_solution='s', target_audience='a',
        )
        self.model = PredictionModel.objects.create(
            name='M', algorithm='XGBoost', version='1.0',
            feature_schema_version='1.0', artifact_path='x', is_active=True,
        )
        StartupFeatureVector.objects.create(
            startup_idea=self.idea,
            schema_version='1.0',
            features={'market_size': 0.8, 'team': 0.6},
        )

    def test_run_prediction(self):
        from ml.services.prediction_service import PredictionService
        result = PredictionService.run_prediction(self.idea)
        self.assertIsNotNone(result)
        self.assertGreater(result.predicted_success_probability, 0)
        self.assertEqual(result.model, self.model)
