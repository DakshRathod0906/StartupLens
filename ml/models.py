import uuid
from django.db import models
from startup_ideas.models import StartupIdea

class PredictionModel(models.Model):
    """
    Registry for Machine Learning models (e.g. XGBoost, Random Forest).
    Allows versioning and swapping of serialized model artifacts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    algorithm = models.CharField(max_length=100) # e.g. "XGBoost", "Random Forest"
    version = models.CharField(max_length=50)
    feature_schema_version = models.CharField(max_length=50)
    
    # Metrics
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    
    artifact_path = models.CharField(max_length=500, help_text="Path to serialized model (e.g., .joblib or .pkl)")
    is_active = models.BooleanField(default=False)
    trained_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'version')

    def __str__(self):
        return f"{self.name} v{self.version} ({self.algorithm})"


class StartupFeatureVector(models.Model):
    """
    Decouples the database schema from the ML inference engine by storing 
    pre-computed numerical/categorical features.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startup_idea = models.ForeignKey(StartupIdea, on_delete=models.CASCADE, related_name="feature_vectors")
    schema_version = models.CharField(max_length=50)
    features = models.JSONField(help_text="Dictionary of engineered features ready for inference")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feature Vector for {self.startup_idea.title} (Schema v{self.schema_version})"


class TrainingRun(models.Model):
    """
    Log of offline model training executions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(PredictionModel, on_delete=models.CASCADE, related_name="training_runs")
    dataset_path = models.CharField(max_length=500)
    parameters = models.JSONField(help_text="Hyperparameters used for training")
    metrics = models.JSONField(help_text="Full training metrics and confusion matrix")
    status = models.CharField(max_length=50, default="PENDING")
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Training Run for {self.model.name} v{self.model.version}"


class PredictionResult(models.Model):
    """
    The output of an ML inference execution.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startup_idea = models.ForeignKey(StartupIdea, on_delete=models.CASCADE, related_name="predictions")
    model = models.ForeignKey(PredictionModel, on_delete=models.PROTECT)
    
    predicted_success_probability = models.FloatField(help_text="Probability between 0.0 and 1.0")
    predicted_failure_probability = models.FloatField(help_text="Probability between 0.0 and 1.0")
    
    feature_importances = models.JSONField(blank=True, default=dict, help_text="Top contributing features for this specific prediction (SHAP values, etc.)")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.startup_idea.title} using {self.model.name}"
