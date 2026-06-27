from django.contrib import admin
from .models import FinalEvaluation, EvaluationSnapshot

@admin.register(FinalEvaluation)
class FinalEvaluationAdmin(admin.ModelAdmin):
    list_display = ('startup_idea', 'version', 'readiness_score', 'readiness_level', 'overall_grade', 'status')
    list_filter = ('readiness_level', 'status', 'overall_grade')
    search_fields = ('startup_idea__title',)
    autocomplete_fields = ('startup_idea', 'overall_assessment', 'recommendation_summary', 'roadmap', 'generated_from_overall_assessment')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(EvaluationSnapshot)
class EvaluationSnapshotAdmin(admin.ModelAdmin):
    list_display = ('final_evaluation', 'overall_score_snapshot', 'overall_grade_snapshot', 'created_at')
    search_fields = ('final_evaluation__startup_idea__title',)
    autocomplete_fields = ('final_evaluation',)
    readonly_fields = ('created_at',)
