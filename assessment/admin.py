from django.contrib import admin
from .models import AssessmentRule, Assessment, OverallAssessment

@admin.register(AssessmentRule)
class AssessmentRuleAdmin(admin.ModelAdmin):
    list_display = ('assessment_type', 'weight', 'minimum_score', 'maximum_score', 'is_active')
    list_filter = ('is_active',)

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'assessment_type', 'percentage', 'grade', 'version', 'status', 'created_at')
    list_filter = ('assessment_type', 'status', 'grade', 'version')
    search_fields = ('summary', 'startup_idea__title')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('startup_idea', 'generated_from_insights')

@admin.register(OverallAssessment)
class OverallAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'startup_idea', 'overall_score', 'grade', 'version', 'created_at')
    list_filter = ('grade', 'version')
    search_fields = ('summary', 'startup_idea__title')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('startup_idea',)
