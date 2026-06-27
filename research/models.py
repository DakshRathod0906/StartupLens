from django.db import models
from .constants import ResearchProvider, ResearchJobStatus, ResearchSourceStatus

class ResearchJob(models.Model):
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='research_jobs'
    )
    status = models.CharField(
        max_length=20,
        choices=ResearchJobStatus.choices,
        default=ResearchJobStatus.PENDING
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    
    total_sources = models.PositiveIntegerField(default=0)
    processed_sources = models.PositiveIntegerField(default=0)
    failed_sources = models.PositiveIntegerField(default=0)
    duplicate_sources = models.PositiveIntegerField(default=0)
    
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['startup_idea']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"ResearchJob #{self.id} for {self.startup_idea.title} - {self.status}"

class ResearchSource(models.Model):
    research_job = models.ForeignKey(
        ResearchJob,
        on_delete=models.CASCADE,
        related_name='sources'
    )
    title = models.CharField(max_length=500)
    original_url = models.URLField(max_length=2000)
    canonical_url = models.URLField(max_length=2000)
    domain = models.CharField(max_length=255)
    
    provider = models.CharField(
        max_length=20,
        choices=ResearchProvider.choices
    )
    status = models.CharField(
        max_length=20,
        choices=ResearchSourceStatus.choices,
        default=ResearchSourceStatus.PENDING
    )
    
    excerpt = models.TextField()
    author = models.CharField(max_length=255, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    credibility_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0
    )
    language = models.CharField(max_length=10, default='en')
    content_hash = models.CharField(max_length=64)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["research_job", "canonical_url"],
                name="unique_job_url"
            )
        ]
        indexes = [
            models.Index(fields=['research_job']),
            models.Index(fields=['provider']),
            models.Index(fields=['domain']),
            models.Index(fields=['published_at']),
            models.Index(fields=['content_hash']),
        ]

    def __str__(self):
        return f"{self.provider}: {self.title}"
