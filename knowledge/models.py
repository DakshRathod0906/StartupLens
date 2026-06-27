from django.db import models
from .constants import FindingType, ProcessingStatus

class Finding(models.Model):
    research_source = models.ForeignKey(
        'research.ResearchSource',
        on_delete=models.CASCADE,
        related_name='findings'
    )
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='findings'
    )
    
    finding_type = models.CharField(
        max_length=50,
        choices=FindingType.choices
    )
    title = models.CharField(max_length=500)
    normalized_title = models.CharField(max_length=500)
    description = models.TextField()
    
    extractor_name = models.CharField(max_length=255)
    processing_status = models.CharField(
        max_length=50,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.PENDING
    )
    
    confidence_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0
    )
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["research_source", "finding_type", "normalized_title"],
                name="unique_finding_per_source"
            )
        ]
        indexes = [
            models.Index(fields=['startup_idea']),
            models.Index(fields=['finding_type']),
            models.Index(fields=['processing_status']),
            models.Index(fields=['confidence_score']),
            models.Index(fields=['created_at']),
            models.Index(fields=['normalized_title']),
        ]

    def __str__(self):
        return f"{self.finding_type}: {self.title}"
