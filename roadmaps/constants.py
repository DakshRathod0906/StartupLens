from django.db import models

class RoadmapStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    SUPERSEDED = "SUPERSEDED", "Superseded"
    ARCHIVED = "ARCHIVED", "Archived"

class RoadmapTaskStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    BLOCKED = "BLOCKED", "Blocked"

class RoadmapPhase(models.TextChoices):
    IMMEDIATE = "IMMEDIATE", "Immediate"
    SHORT_TERM = "SHORT_TERM", "Short Term"
    MEDIUM_TERM = "MEDIUM_TERM", "Medium Term"
    LONG_TERM = "LONG_TERM", "Long Term"
