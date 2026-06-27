from django.db import models

class RecommendationPriority(models.TextChoices):
    CRITICAL = "CRITICAL", "Critical"
    HIGH = "HIGH", "High"
    MEDIUM = "MEDIUM", "Medium"
    LOW = "LOW", "Low"
    OPTIONAL = "OPTIONAL", "Optional"

class RecommendationStatus(models.TextChoices):
    GENERATED = "GENERATED", "Generated"
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Completed"
    SUPERSEDED = "SUPERSEDED", "Superseded"
    ARCHIVED = "ARCHIVED", "Archived"

class RecommendationCategory(models.TextChoices):
    MARKET = "MARKET", "Market"
    COMPETITION = "COMPETITION", "Competition"
    TECHNOLOGY = "TECHNOLOGY", "Technology"
    FUNDING = "FUNDING", "Funding"
    RISK = "RISK", "Risk"
    EXECUTION = "EXECUTION", "Execution"
    OVERALL = "OVERALL", "Overall"

class RuleOperator(models.TextChoices):
    LT = "<", "Less Than"
    LTE = "<=", "Less Than or Equal"
    GT = ">", "Greater Than"
    GTE = ">=", "Greater Than or Equal"
    EQ = "=", "Equal"
    BETWEEN = "BETWEEN", "Between"

class RuleGroupChoices(models.TextChoices):
    GROWTH = "GROWTH", "Growth"
    FUNDING = "FUNDING", "Funding"
    TECHNOLOGY = "TECHNOLOGY", "Technology"
    COMPETITION = "COMPETITION", "Competition"
    EXECUTION = "EXECUTION", "Execution"
    RISK = "RISK", "Risk"

METRIC_REGISTRY = {
    "market_percentage": "Market Percentage",
    "competition_percentage": "Competition Percentage",
    "demand_percentage": "Demand Percentage",
    "business_model_percentage": "Business Model Percentage",
    "revenue_percentage": "Revenue Percentage",
    "technology_percentage": "Technology Percentage",
    "execution_percentage": "Execution Percentage",
    "scalability_percentage": "Scalability Percentage",
    "risk_percentage": "Risk Percentage",
    "overall_score": "Overall Score",
}

def get_metric_choices():
    return [(k, v) for k, v in METRIC_REGISTRY.items()]
