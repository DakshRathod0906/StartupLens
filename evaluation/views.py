from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from .models import FinalEvaluation

class DashboardView(TemplateView):
    template_name = 'evaluation/dashboard.html'

class EvaluationDetailView(DetailView):
    model = FinalEvaluation
    template_name = 'evaluation/evaluation_detail.html'
    context_object_name = 'evaluation'

class EvaluationHistoryView(ListView):
    model = FinalEvaluation
    template_name = 'evaluation/evaluation_history.html'
    context_object_name = 'evaluations'
    
class ExecutiveSummaryView(DetailView):
    model = FinalEvaluation
    template_name = 'evaluation/executive_summary.html'
    context_object_name = 'evaluation'

class DecisionBreakdownView(DetailView):
    model = FinalEvaluation
    template_name = 'evaluation/decision_breakdown.html'
    context_object_name = 'evaluation'
