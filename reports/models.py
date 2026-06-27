import uuid
from django.db import models
from django.conf import settings

class ReportTemplate(models.Model):
    """
    Template definition for generating PDF reports.
    Versioning allows historical reports to remain reproducible.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'version')

    def __str__(self):
        return f"{self.name} (v{self.version})"


class ReportSection(models.Model):
    """
    Defines the layout and inclusion of sections within a report template.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    content_type = models.CharField(max_length=100) # e.g., 'executive_summary', 'financials', 'roadmap'
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.template.name} - {self.title}"


class Report(models.Model):
    """
    Generated PDF report instances based strictly on immutable snapshots.
    """
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        GENERATING = "GENERATING", "Generating"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evaluation_snapshot = models.ForeignKey(
        'evaluation.EvaluationSnapshot', 
        on_delete=models.PROTECT, 
        related_name="reports"
    )
    report_template = models.ForeignKey(ReportTemplate, on_delete=models.PROTECT)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.PENDING
    )
    file_path = models.FileField(upload_to="reports/pdfs/", null=True, blank=True)
    checksum = models.CharField(max_length=64, blank=True, help_text="SHA-256 checksum for integrity verification")
    version = models.PositiveIntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report {self.id} for Snapshot {self.evaluation_snapshot.id}"
