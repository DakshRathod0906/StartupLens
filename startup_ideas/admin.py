from django.contrib import admin
from .models import StartupIdea, Tag, Industry

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)

@admin.register(StartupIdea)
class StartupIdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'startup_stage', 'industry', 'created_at')
    list_filter = ('status', 'startup_stage', 'industry', 'is_deleted')
    search_fields = ('title', 'short_description', 'owner__username', 'slug')
    autocomplete_fields = ['owner', 'industry', 'tags']
    filter_horizontal = ['tags']
    readonly_fields = ('slug', 'created_at', 'updated_at', 'archived_at', 'deleted_at', 'last_analyzed_at')
    
    fieldsets = (
        (None, {
            'fields': ('owner', 'title', 'slug', 'status', 'startup_stage', 'industry', 'tags', 'version')
        }),
        ('Details', {
            'fields': ('short_description', 'problem_statement', 'proposed_solution', 'target_audience', 'business_model', 'revenue_model')
        }),
        ('State & Audit', {
            'fields': ('is_deleted', 'deleted_at', 'archived_at', 'last_analyzed_at', 'created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        return self.model.all_objects.all()
