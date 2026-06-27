from django.db import models

class InsightType(models.TextChoices):
    COMPETITION = "COMPETITION", "Competition"
    MARKET = "MARKET", "Market"
    PRICING = "PRICING", "Pricing"
    DEMAND = "DEMAND", "Demand"
    TARGET_AUDIENCE = "TARGET_AUDIENCE", "Target Audience"
    TECHNOLOGY = "TECHNOLOGY", "Technology"
    FUNDING = "FUNDING", "Funding"
    REGULATION = "REGULATION", "Regulation"
    RISK = "RISK", "Risk"
    OPPORTUNITY = "OPPORTUNITY", "Opportunity"
    BUSINESS_MODEL = "BUSINESS_MODEL", "Business Model"

class InsightStatus(models.TextChoices):
    GENERATED = "GENERATED", "Generated"
    VERIFIED = "VERIFIED", "Verified"
    STALE = "STALE", "Stale"
