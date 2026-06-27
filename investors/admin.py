from django.contrib import admin
from investors.models import Investor, InvestmentPreference, StartupInvestorMatch, MatchExplanation

@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_active', 'created_at')

@admin.register(InvestmentPreference)
class InvestmentPreferenceAdmin(admin.ModelAdmin):
    list_display = ('investor', 'ticket_size_min', 'ticket_size_max', 'risk_appetite')

@admin.register(StartupInvestorMatch)
class StartupInvestorMatchAdmin(admin.ModelAdmin):
    list_display = ('startup_idea', 'investor', 'compatibility_score', 'match_status', 'matched_at')
    list_filter = ('match_status',)

@admin.register(MatchExplanation)
class MatchExplanationAdmin(admin.ModelAdmin):
    list_display = ('match', 'matched_stage', 'matched_budget')
