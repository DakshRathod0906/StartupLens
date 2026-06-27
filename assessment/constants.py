from django.db import models

class AssessmentType(models.TextChoices):
    MARKET = "MARKET", "Market"
    COMPETITION = "COMPETITION", "Competition"
    DEMAND = "DEMAND", "Demand"
    BUSINESS_MODEL = "BUSINESS_MODEL", "Business Model"
    REVENUE = "REVENUE", "Revenue"
    TECHNOLOGY = "TECHNOLOGY", "Technology"
    EXECUTION = "EXECUTION", "Execution"
    SCALABILITY = "SCALABILITY", "Scalability"
    RISK = "RISK", "Risk"

class AssessmentStatus(models.TextChoices):
    GENERATED = "GENERATED", "Generated"
    SUPERSEDED = "SUPERSEDED", "Superseded"
