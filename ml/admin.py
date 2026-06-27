from django.contrib import admin
from ml.models import PredictionModel, PredictionResult, TrainingRun, StartupFeatureVector


@admin.register(PredictionModel)
class PredictionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'algorithm', 'version', 'accuracy', 'f1_score', 'is_active', 'trained_at')
    list_filter = ('algorithm', 'is_active')
    search_fields = ('name',)


@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = ('startup_idea', 'model', 'predicted_success_probability', 'created_at')
    list_filter = ('model',)


@admin.register(TrainingRun)
class TrainingRunAdmin(admin.ModelAdmin):
    list_display = ('model', 'status', 'started_at', 'completed_at')
    list_filter = ('status',)


@admin.register(StartupFeatureVector)
class StartupFeatureVectorAdmin(admin.ModelAdmin):
    list_display = ('startup_idea', 'schema_version', 'created_at')
