from django.contrib import admin
from .models import ResearchJob, ResearchSource

@admin.register(ResearchJob)
class ResearchJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'startup_idea', 'status', 'total_sources', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('startup_idea__title', 'error_message')

@admin.register(ResearchSource)
class ResearchSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'provider', 'domain', 'status', 'credibility_score', 'created_at')
    list_filter = ('provider', 'status', 'created_at')
    search_fields = ('title', 'canonical_url', 'domain')
    readonly_fields = ('content_hash',)
