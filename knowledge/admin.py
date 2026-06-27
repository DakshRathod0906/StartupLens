from django.contrib import admin
from .models import Finding

@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ('id', 'finding_type', 'title', 'confidence_score', 'processing_status', 'created_at')
    list_filter = ('finding_type', 'processing_status', 'created_at', 'extractor_name')
    search_fields = ('title', 'normalized_title', 'description', 'startup_idea__title')
    readonly_fields = ('created_at', 'updated_at')
