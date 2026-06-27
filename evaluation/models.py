from django.db import models
from django.conf import settings
from .constants import ReadinessLevel, EvaluationStatus, AnalysisStepStatus

class FinalEvaluation(models.Model):
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='evaluations'
    )
    generated_from_overall_assessment = models.ForeignKey(
        'assessment.OverallAssessment',
        on_delete=models.PROTECT,
        related_name="generated_evaluations",
        null=True, blank=True
    )
    overall_assessment = models.OneToOneField(
        'assessment.OverallAssessment',
        on_delete=models.PROTECT,
        related_name='final_evaluation',
        null=True, blank=True
    )
    recommendation_summary = models.OneToOneField(
        'recommendations.RecommendationSummary',
        on_delete=models.PROTECT,
        related_name='final_evaluation',
        null=True, blank=True
    )
    roadmap = models.OneToOneField(
        'roadmaps.Roadmap',
        on_delete=models.PROTECT,
        related_name='final_evaluation',
        null=True, blank=True
    )
    readiness_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    readiness_level = models.CharField(max_length=50, choices=ReadinessLevel.choices)
    overall_grade = models.CharField(max_length=2)
    executive_summary = models.TextField()
    key_strengths = models.JSONField(default=list)
    key_risks = models.JSONField(default=list)
    critical_actions = models.JSONField(default=list)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50, choices=EvaluationStatus.choices, default=EvaluationStatus.GENERATED)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['startup_idea', 'version'],
                name='unique_evaluation_version'
            )
        ]
        ordering = ['-version']

    def __str__(self):
        return f"Evaluation v{self.version} for {self.startup_idea.title} - {self.get_readiness_level_display()}"


class EvaluationSnapshot(models.Model):
    final_evaluation = models.OneToOneField(
        FinalEvaluation,
        on_delete=models.CASCADE,
        related_name='snapshot'
    )
    assessment_snapshot = models.JSONField(default=dict)
    recommendation_snapshot = models.JSONField(default=dict)
    roadmap_snapshot = models.JSONField(default=dict)
    strength_snapshot = models.JSONField(default=dict)
    risk_snapshot = models.JSONField(default=dict)
    summary_snapshot = models.JSONField(default=dict)
    overall_score_snapshot = models.DecimalField(max_digits=5, decimal_places=2)
    overall_grade_snapshot = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Snapshot of Evaluation v{self.final_evaluation.version}"

class AnalysisRun(models.Model):
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='analysis_runs'
    )
    from startup_ideas.constants import AnalysisStatus
    status = models.CharField(max_length=20, choices=AnalysisStatus.choices, default=AnalysisStatus.PENDING)
    progress = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    triggered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='triggered_analysis_runs'
    )

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Run {self.id} for {self.startup_idea.title} - {self.get_status_display()}"


class AnalysisStep(models.Model):
    run = models.ForeignKey(
        AnalysisRun,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    startup_idea = models.ForeignKey(
        'startup_ideas.StartupIdea',
        on_delete=models.CASCADE,
        related_name='analysis_steps'
    )
    step_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=AnalysisStepStatus.choices, default=AnalysisStepStatus.PENDING)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['started_at']
        constraints = [
            models.UniqueConstraint(fields=['run', 'step_name'], name='unique_step_per_run')
        ]

    def __str__(self):
        return f"{self.step_name} - {self.get_status_display()} ({self.startup_idea.title})"
