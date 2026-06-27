from ml.models import StartupFeatureVector, PredictionResult
from ml.inference.loader import ModelLoader
from ml.inference.predictor import Predictor
from startup_ideas.models import StartupIdea

class PredictionService:
    """
    Coordinates the inference flow for a StartupIdea.
    """
    
    @staticmethod
    def run_prediction(startup_idea: StartupIdea) -> PredictionResult:
        """
        Generates a PredictionResult for the given startup idea using the active ML model.
        """
        # 1. Load active model from registry
        db_model, ml_artifact = ModelLoader.load_active_model()
        
        # 2. Get latest feature vector
        vector = StartupFeatureVector.objects.filter(
            startup_idea=startup_idea,
            schema_version=db_model.feature_schema_version
        ).order_by('-created_at').first()
        
        if not vector:
            raise ValueError(f"No FeatureVector (v{db_model.feature_schema_version}) found for StartupIdea {startup_idea.id}")
            
        # 3. Predict
        predictor = Predictor(ml_artifact)
        success_prob, fail_prob, importances = predictor.predict(vector.features)
        
        # 4. Save result
        result = PredictionResult.objects.create(
            startup_idea=startup_idea,
            model=db_model,
            predicted_success_probability=success_prob,
            predicted_failure_probability=fail_prob,
            feature_importances=importances
        )
        return result
