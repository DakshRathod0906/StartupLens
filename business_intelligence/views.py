from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Insight
from .services import DashboardService

@login_required
def dashboard_view(request):
    stats = DashboardService.get_statistics()
    return render(request, 'business_intelligence/dashboard.html', {'stats': stats})

@login_required
def insight_list_view(request):
    insights = Insight.objects.select_related('startup_idea').order_by('-created_at')
    return render(request, 'business_intelligence/insight_list.html', {'insights': insights})

@login_required
def insight_detail_view(request, insight_id):
    insight = get_object_or_404(Insight, id=insight_id)
    return render(request, 'business_intelligence/insight_detail.html', {'insight': insight})
