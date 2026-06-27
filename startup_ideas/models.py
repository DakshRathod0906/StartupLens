from django.db import models
from django.conf import settings
from django.urls import reverse
from .constants import StartupIdeaStatus, StartupStage, AnalysisStatus
from .managers import StartupIdeaManager, StartupIdeaAllManager

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_tag_slug')
        ]

    def __str__(self):
        return self.name

class Industry(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class for icon, e.g., 'bi bi-heart'")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_industry_slug')
        ]
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name

class StartupIdea(models.Model):
    # Core Fields
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='startup_ideas')
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200)
    short_description = models.CharField(max_length=300)
    problem_statement = models.TextField()
    proposed_solution = models.TextField()
    target_audience = models.TextField()
    business_model = models.TextField(blank=True)
    revenue_model = models.TextField(blank=True)
    
    # Relations
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, related_name='startup_ideas')
    tags = models.ManyToManyField(Tag, blank=True, related_name='startup_ideas')
    
    # Metadata Fields
    status = models.CharField(max_length=20, choices=StartupIdeaStatus.choices, default=StartupIdeaStatus.DRAFT)
    startup_stage = models.CharField(max_length=20, choices=StartupStage.choices, default=StartupStage.IDEA)
    
    # State / Metadata Fields
    archived_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Analysis Fields
    analysis_status = models.CharField(max_length=20, choices=AnalysisStatus.choices, default=AnalysisStatus.PENDING)
    analysis_progress = models.PositiveIntegerField(default=0)
    analysis_started_at = models.DateTimeField(null=True, blank=True)
    analysis_completed_at = models.DateTimeField(null=True, blank=True)
    last_analyzed_at = models.DateTimeField(null=True, blank=True)
    
    version = models.PositiveIntegerField(default=1)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StartupIdeaManager()
    all_objects = StartupIdeaAllManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'slug'], name='unique_owner_slug')
        ]
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['status']),
            models.Index(fields=['industry']),
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('startup_ideas:detail', kwargs={'slug': self.slug})
