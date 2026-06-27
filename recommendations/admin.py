from django.contrib import admin
from .models import RecommendationRule, Recommendation, RecommendationSummary

@admin.register(RecommendationRule)
class RecommendationRuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'metric', 'operator', 'minimum_value', 'maximum_value', 'priority', 'rule_group', 'is_active', 'display_order')
    list_filter = ('is_active', 'priority', 'rule_group', 'metric')
    search_fields = ('title', 'description')

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'startup_idea', 'priority', 'category', 'status', 'version', 'is_resolved', 'created_at')
    list_filter = ('priority', 'category', 'status', 'is_resolved')
    search_fields = ('title', 'startup_idea__title')
    autocomplete_fields = ('startup_idea', 'assessment', 'matched_rule')

@admin.register(RecommendationSummary)
class RecommendationSummaryAdmin(admin.ModelAdmin):
    list_display = ('startup_idea', 'overall_priority', 'total_recommendations', 'version', 'created_at')
    list_filter = ('overall_priority',)
    search_fields = ('startup_idea__title',)
    autocomplete_fields = ('startup_idea', 'overall_assessment')
