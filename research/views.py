from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ResearchJob, ResearchSource
from .services import DashboardService, ResearchService

@login_required
def dashboard_view(request):
    stats = DashboardService.get_statistics()
    return render(request, 'research/dashboard.html', {'stats': stats})

@login_required
def job_list_view(request):
    # Depending on implementation, you might want to filter by user's ideas,
    # but for now we just show all jobs to admins or owners.
    jobs = ResearchJob.objects.select_related('startup_idea').order_by('-created_at')
    return render(request, 'research/job_list.html', {'jobs': jobs})

@login_required
def job_detail_view(request, job_id):
    job = get_object_or_404(ResearchJob, id=job_id)
    sources = job.sources.all().order_by('-credibility_score')
    return render(request, 'research/job_detail.html', {'job': job, 'sources': sources})

@login_required
def source_list_view(request):
    sources = ResearchSource.objects.select_related('research_job').order_by('-created_at')
    return render(request, 'research/source_list.html', {'sources': sources})

@login_required
def source_detail_view(request, source_id):
    source = get_object_or_404(ResearchSource, id=source_id)
    return render(request, 'research/source_detail.html', {'source': source})
