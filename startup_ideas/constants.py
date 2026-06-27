from django.db import models

class StartupIdeaStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    ARCHIVED = "ARCHIVED", "Archived"

class StartupStage(models.TextChoices):
    IDEA = "IDEA", "Idea"
    VALIDATION = "VALIDATION", "Validation"
    MVP = "MVP", "MVP"
    GROWTH = "GROWTH", "Growth"
