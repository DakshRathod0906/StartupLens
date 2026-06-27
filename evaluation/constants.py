from django.db import models

class ReadinessLevel(models.TextChoices):
    NOT_READY = "NOT_READY", "Not Ready"
    EARLY_STAGE = "EARLY_STAGE", "Early Stage"
    PROMISING = "PROMISING", "Promising"
    INVESTMENT_READY = "INVESTMENT_READY", "Investment Ready"

class EvaluationStatus(models.TextChoices):
    GENERATED = "GENERATED", "Generated"
    SUPERSEDED = "SUPERSEDED", "Superseded"
