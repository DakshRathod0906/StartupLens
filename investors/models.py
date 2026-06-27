import uuid
from django.db import models
from startup_ideas.models import StartupIdea

class Investor(models.Model):
    """
    Represents an individual investor, VC firm, or incubator/funding program.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class InvestmentPreference(models.Model):
    """
    Normalized investment preferences for matching logic.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    investor = models.OneToOneField(Investor, on_delete=models.CASCADE, related_name="preferences")
    industry = models.JSONField(default=list, help_text="List of preferred industries")
    stage = models.JSONField(default=list, help_text="List of preferred funding stages")
    country = models.JSONField(default=list, help_text="List of preferred countries/regions")
    ticket_size_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ticket_size_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    risk_appetite = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.investor.name}"


class StartupInvestorMatch(models.Model):
    """
    Represents a potential funding match between a startup idea and an investor.
    """
    class MatchStatusChoices(models.TextChoices):
        SUGGESTED = "SUGGESTED", "Suggested"
        CONTACTED = "CONTACTED", "Contacted"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startup_idea = models.ForeignKey(StartupIdea, on_delete=models.CASCADE, related_name="investor_matches")
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="startup_matches")
    compatibility_score = models.IntegerField(help_text="Match score from 0-100")
    match_status = models.CharField(
        max_length=20, 
        choices=MatchStatusChoices.choices, 
        default=MatchStatusChoices.SUGGESTED
    )
    matched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('startup_idea', 'investor')

    def __str__(self):
        return f"{self.startup_idea.title} <-> {self.investor.name} ({self.compatibility_score}%)"


class MatchExplanation(models.Model):
    """
    Explanation of why an investor matched with a startup.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.OneToOneField(StartupInvestorMatch, on_delete=models.CASCADE, related_name="explanation")
    matched_industries = models.JSONField(default=list)
    matched_stage = models.BooleanField(default=False)
    matched_budget = models.BooleanField(default=False)
    reasoning = models.TextField(help_text="Detailed explanation of the match rationale")

    def __str__(self):
        return f"Explanation for Match {self.match.id}"
