from django.db import models
from .constants import InsightType, InsightStatus

class Insight(models.Model):
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='insights'
    )
    generated_from_job = models.ForeignKey(
        'research.ResearchJob',
        on_delete=models.CASCADE,
        related_name='insights'
    )
    insight_type = models.CharField(
        max_length=50,
        choices=InsightType.choices
    )
    status = models.CharField(
        max_length=50,
        choices=InsightStatus.choices,
        default=InsightStatus.GENERATED
    )
    title = models.CharField(max_length=500)
    summary = models.TextField()
    confidence_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0
    )
    version = models.PositiveIntegerField(default=1)
    
    supporting_findings = models.ManyToManyField(
        'knowledge.Finding',
        related_name='supported_insights'
    )
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["startup_idea", "insight_type", "title", "version"],
                name="unique_insight_version"
            )
        ]
        indexes = [
            models.Index(fields=['startup_idea']),
            models.Index(fields=['generated_from_job']),
            models.Index(fields=['insight_type']),
            models.Index(fields=['status']),
            models.Index(fields=['confidence_score']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.insight_type} v{self.version}: {self.title}"
