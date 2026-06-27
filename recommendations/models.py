from django.db import models
from .constants import (
    RecommendationPriority,
    RecommendationStatus,
    RecommendationCategory,
    RuleOperator,
    RuleGroupChoices,
    get_metric_choices
)

class RecommendationRule(models.Model):
    metric = models.CharField(max_length=50, choices=get_metric_choices())
    operator = models.CharField(max_length=10, choices=RuleOperator.choices)
    minimum_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    maximum_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=RecommendationPriority.choices)
    rule_group = models.CharField(max_length=50, choices=RuleGroupChoices.choices)
    title = models.CharField(max_length=200)
    description = models.TextField()
    recommended_action = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["metric", "operator", "minimum_value", "maximum_value", "display_order"],
                name="unique_recommendation_rule"
            )
        ]
        ordering = ['display_order']

    def __str__(self):
        return f"{self.get_metric_display()} {self.operator} - {self.priority}"

class Recommendation(models.Model):
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    assessment = models.ForeignKey(
        'assessment.Assessment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='triggered_recommendations'
    )
    matched_rule = models.ForeignKey(
        RecommendationRule,
        on_delete=models.PROTECT,
        related_name='generated_recommendations'
    )
    priority = models.CharField(max_length=20, choices=RecommendationPriority.choices)
    category = models.CharField(max_length=50, choices=RecommendationCategory.choices)
    status = models.CharField(max_length=50, choices=RecommendationStatus.choices, default=RecommendationStatus.GENERATED)
    title = models.CharField(max_length=200)
    description = models.TextField()
    recommended_action = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    version = models.PositiveIntegerField(default=1)
    
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["startup_idea", "matched_rule", "version"],
                name="unique_startup_rule_version"
            )
        ]
        indexes = [
            models.Index(fields=['startup_idea']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f"{self.startup_idea.title} - {self.title} (v{self.version})"

class RecommendationSummary(models.Model):
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='recommendation_summaries'
    )
    overall_assessment = models.ForeignKey(
        'assessment.OverallAssessment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    overall_priority = models.CharField(max_length=20, choices=RecommendationPriority.choices)
    executive_summary = models.TextField()
    
    total_recommendations = models.PositiveIntegerField(default=0)
    critical_count = models.PositiveIntegerField(default=0)
    high_count = models.PositiveIntegerField(default=0)
    medium_count = models.PositiveIntegerField(default=0)
    low_count = models.PositiveIntegerField(default=0)
    optional_count = models.PositiveIntegerField(default=0)
    
    version = models.PositiveIntegerField(default=1)
    overall_score_snapshot = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    overall_grade_snapshot = models.CharField(max_length=20, null=True, blank=True)
    assessment_version = models.PositiveIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary v{self.version} for {self.startup_idea.title}"
