from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recommendation, RecommendationSummary
from .services import DashboardService

@login_required
def dashboard_view(request):
    stats = DashboardService.get_statistics()
    return render(request, 'recommendations/dashboard.html', {'stats': stats})

@login_required
def recommendation_list_view(request):
    summaries = RecommendationSummary.objects.select_related('startup_idea').order_by('-created_at')
    active_recs = Recommendation.objects.select_related('startup_idea').filter(status='ACTIVE').order_by('-created_at')
    return render(request, 'recommendations/recommendation_list.html', {
        'summaries': summaries,
        'active_recs': active_recs
    })

@login_required
def recommendation_detail_view(request, recommendation_id):
    rec = get_object_or_404(Recommendation, id=recommendation_id)
    return render(request, 'recommendations/recommendation_detail.html', {'rec': rec})

@login_required
def recommendation_history_view(request, recommendation_id):
    rec = get_object_or_404(Recommendation, id=recommendation_id)
    history = Recommendation.objects.filter(
        startup_idea=rec.startup_idea,
        matched_rule=rec.matched_rule
    ).order_by('-version')
    return render(request, 'recommendations/recommendation_history.html', {
        'current': rec,
        'history': history
    })

@login_required
def summary_view(request, summary_id):
    summary = get_object_or_404(RecommendationSummary, id=summary_id)
    return render(request, 'recommendations/summary.html', {'summary': summary})
