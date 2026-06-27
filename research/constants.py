from django.db import models

class ResearchProvider(models.TextChoices):
    GOOGLE = "GOOGLE", "Google"
    REDDIT = "REDDIT", "Reddit"
    GITHUB = "GITHUB", "GitHub"
    NEWS = "NEWS", "News"
    WEBSITE = "WEBSITE", "Website"

class ResearchJobStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    RUNNING = "RUNNING", "Running"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"

class ResearchSourceStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    NORMALIZED = "NORMALIZED", "Normalized"
    FAILED = "FAILED", "Failed"
    SKIPPED = "SKIPPED", "Skipped"
