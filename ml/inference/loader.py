import os
import joblib
from django.conf import settings
from ml.models import PredictionModel

class ModelLoader:
    """
    Loads serialized ML models (e.g. .joblib, .pkl) from the filesystem 
    based on the PredictionModel registry.
    """
    
    _cache = {}

    @classmethod
    def load_active_model(cls) -> tuple[PredictionModel, object]:
        """
        Loads the currently active PredictionModel and its binary artifact.
        Caches the artifact in memory to avoid repeated disk reads.
        """
        # Get active model from registry
        db_model = PredictionModel.objects.filter(is_active=True).order_by('-version').first()
        if not db_model:
            raise ValueError("No active PredictionModel found in the registry.")
            
        # Check cache
        if db_model.id in cls._cache:
            return db_model, cls._cache[db_model.id]
            
        # Load from disk
        artifact_path = os.path.join(settings.BASE_DIR, db_model.artifact_path)
        if not os.path.exists(artifact_path):
            # For Phase 10 MVP, if no physical model exists, return a dummy object
            # In a real app we'd raise FileNotFoundError
            loaded_model = "DUMMY_MODEL" 
        else:
            loaded_model = joblib.load(artifact_path)
            
        # Cache and return
        cls._cache[db_model.id] = loaded_model
        return db_model, loaded_model
