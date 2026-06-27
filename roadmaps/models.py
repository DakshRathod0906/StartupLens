from django.db import models
from recommendations.constants import RecommendationPriority
from .constants import RoadmapStatus, RoadmapTaskStatus, RoadmapPhase

class TaskTemplate(models.Model):
    recommendation_rule = models.OneToOneField(
        'recommendations.RecommendationRule',
        on_delete=models.CASCADE,
        related_name='task_template'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_days = models.PositiveIntegerField(default=1)
    default_priority = models.CharField(max_length=20, choices=RecommendationPriority.choices, default=RecommendationPriority.MEDIUM)
    default_phase = models.CharField(max_length=50, choices=RoadmapPhase.choices, default=RoadmapPhase.MEDIUM_TERM)
    depends_on = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependent_templates')
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recommendation_rule', 'title'],
                name='unique_task_template'
            )
        ]

    def __str__(self):
        return self.title

class Roadmap(models.Model):
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='roadmaps'
    )
    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50, choices=RoadmapStatus.choices, default=RoadmapStatus.ACTIVE)
    summary = models.TextField(blank=True)
    total_tasks = models.PositiveIntegerField(default=0)
    completed_tasks = models.PositiveIntegerField(default=0)
    blocked_tasks = models.PositiveIntegerField(default=0)
    critical_tasks = models.PositiveIntegerField(default=0)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    overall_duration_days = models.PositiveIntegerField(default=0)
    estimated_completion = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['startup_idea', 'version'],
                name='unique_roadmap_version'
            )
        ]

    def __str__(self):
        return f"{self.startup_idea.title} - v{self.version}"

class RoadmapTask(models.Model):
    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    recommendation = models.ForeignKey(
        'recommendations.Recommendation',
        on_delete=models.CASCADE,
        related_name='roadmap_tasks',
        null=True, blank=True
    )
    recommendation_title_snapshot = models.CharField(max_length=200, blank=True)
    recommendation_priority_snapshot = models.CharField(max_length=20, blank=True)
    task_template = models.ForeignKey(
        TaskTemplate,
        on_delete=models.PROTECT,
        related_name='generated_tasks'
    )
    phase = models.CharField(max_length=50, choices=RoadmapPhase.choices)
    dependency_level = models.PositiveIntegerField(default=0)
    execution_order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_days = models.PositiveIntegerField(default=1)
    scheduled_start_day = models.PositiveIntegerField(default=1)
    scheduled_end_day = models.PositiveIntegerField(default=1)
    priority = models.CharField(max_length=20, choices=RecommendationPriority.choices)
    status = models.CharField(max_length=50, choices=RoadmapTaskStatus.choices, default=RoadmapTaskStatus.PENDING)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependent_tasks')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['roadmap', 'task_template'],
                name='unique_roadmap_task_template'
            )
        ]
        ordering = ['phase', 'dependency_level', 'execution_order']

    def __str__(self):
        return f"{self.title} ({self.phase})"

class RoadmapProgress(models.Model):
    roadmap = models.OneToOneField(
        Roadmap,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    total_tasks = models.PositiveIntegerField(default=0)
    completed_tasks = models.PositiveIntegerField(default=0)
    blocked_tasks = models.PositiveIntegerField(default=0)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    remaining_days = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress for {self.roadmap}"
