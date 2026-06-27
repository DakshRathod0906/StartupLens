from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Finding
from .services import DashboardService

@login_required
def dashboard_view(request):
    stats = DashboardService.get_statistics()
    return render(request, 'knowledge/dashboard.html', {'stats': stats})

@login_required
def finding_list_view(request):
    findings = Finding.objects.select_related('research_source', 'startup_idea').order_by('-created_at')
    return render(request, 'knowledge/finding_list.html', {'findings': findings})

@login_required
def finding_detail_view(request, finding_id):
    finding = get_object_or_404(Finding, id=finding_id)
    return render(request, 'knowledge/finding_detail.html', {'finding': finding})
