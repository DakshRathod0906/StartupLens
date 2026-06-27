from django.contrib import admin
from .models import TaskTemplate, Roadmap, RoadmapTask

@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'recommendation_rule', 'estimated_days', 'default_priority', 'default_phase', 'is_active')
    list_filter = ('is_active', 'default_priority', 'default_phase')
    search_fields = ('title', 'recommendation_rule__title')
    autocomplete_fields = ('recommendation_rule',)
    filter_horizontal = ('depends_on',)

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('startup_idea', 'version', 'status', 'total_tasks', 'completion_percentage', 'created_at')
    list_filter = ('status',)
    search_fields = ('startup_idea__title',)
    autocomplete_fields = ('startup_idea',)
    readonly_fields = ('total_tasks', 'completed_tasks', 'blocked_tasks', 'critical_tasks', 'completion_percentage', 'overall_duration_days', 'estimated_completion')

@admin.register(RoadmapTask)
class RoadmapTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'roadmap', 'phase', 'dependency_level', 'execution_order', 'priority', 'status')
    list_filter = ('phase', 'status', 'priority')
    search_fields = ('title', 'roadmap__startup_idea__title')
    autocomplete_fields = ('roadmap', 'recommendation', 'task_template')
    filter_horizontal = ('dependencies',)
