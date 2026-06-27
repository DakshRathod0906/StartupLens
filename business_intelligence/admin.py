from django.contrib import admin
from .models import Insight

@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ('id', 'insight_type', 'title', 'version', 'status', 'confidence_score', 'created_at')
    list_filter = ('insight_type', 'status', 'created_at', 'version')
    search_fields = ('title', 'summary', 'startup_idea__title')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('startup_idea', 'generated_from_job', 'supporting_findings')
