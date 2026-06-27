from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assessment, OverallAssessment
from .services import DashboardService

@login_required
def dashboard_view(request):
    stats = DashboardService.get_statistics()
    return render(request, 'assessment/dashboard.html', {'stats': stats})

@login_required
def assessment_list_view(request):
    overall = OverallAssessment.objects.select_related('startup_idea').order_by('-created_at')
    categories = Assessment.objects.select_related('startup_idea').order_by('-created_at')
    return render(request, 'assessment/assessment_list.html', {
        'overall': overall,
        'categories': categories
    })

@login_required
def assessment_detail_view(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    return render(request, 'assessment/assessment_detail.html', {'assessment': assessment})

@login_required
def assessment_history_view(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    history = Assessment.objects.filter(
        startup_idea=assessment.startup_idea,
        assessment_type=assessment.assessment_type
    ).order_by('-version')
    return render(request, 'assessment/assessment_history.html', {
        'current': assessment,
        'history': history
    })
