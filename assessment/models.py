from django.db import models
from .constants import AssessmentType, AssessmentStatus

class AssessmentRule(models.Model):
    assessment_type = models.CharField(
        max_length=50,
        choices=AssessmentType.choices,
        unique=True
    )
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    minimum_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    maximum_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.assessment_type} Rule (Weight: {self.weight}%)"

class Assessment(models.Model):
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='category_assessments'
    )
    assessment_type = models.CharField(
        max_length=50,
        choices=AssessmentType.choices
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=20)
    summary = models.TextField()
    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    status = models.CharField(
        max_length=50,
        choices=AssessmentStatus.choices,
        default=AssessmentStatus.GENERATED
    )
    version = models.PositiveIntegerField(default=1)
    
    generated_from_insights = models.ManyToManyField(
        'business_intelligence.Insight',
        related_name='supported_assessments'
    )
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["startup_idea", "assessment_type", "version"],
                name="unique_assessment_version"
            )
        ]
        indexes = [
            models.Index(fields=['startup_idea']),
            models.Index(fields=['assessment_type']),
            models.Index(fields=['status']),
            models.Index(fields=['percentage']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.assessment_type} v{self.version}: {self.percentage}%"

class OverallAssessment(models.Model):
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='overall_assessments'
    )
    overall_score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=20)
    version = models.PositiveIntegerField(default=1)
    summary = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["startup_idea", "version"],
                name="unique_overall_version"
            )
        ]

    def __str__(self):
        return f"Overall v{self.version} - {self.overall_score}%"
