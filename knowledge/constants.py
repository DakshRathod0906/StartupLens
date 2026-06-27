from django.db import models

class FindingType(models.TextChoices):
    COMPETITOR = "COMPETITOR", "Competitor"
    MARKET_SIZE = "MARKET_SIZE", "Market Size"
    MARKET_TREND = "MARKET_TREND", "Market Trend"
    USER_PAIN_POINT = "USER_PAIN_POINT", "User Pain Point"
    USER_DEMAND = "USER_DEMAND", "User Demand"
    TARGET_AUDIENCE = "TARGET_AUDIENCE", "Target Audience"
    PRICING = "PRICING", "Pricing"
    BUSINESS_MODEL = "BUSINESS_MODEL", "Business Model"
    TECHNOLOGY = "TECHNOLOGY", "Technology"
    REGULATION = "REGULATION", "Regulation"
    FUNDING = "FUNDING", "Funding"
    OPPORTUNITY = "OPPORTUNITY", "Opportunity"
    RISK = "RISK", "Risk"
    OTHER = "OTHER", "Other"

class ProcessingStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    EXTRACTED = "EXTRACTED", "Extracted"
    SKIPPED = "SKIPPED", "Skipped"
    FAILED = "FAILED", "Failed"
