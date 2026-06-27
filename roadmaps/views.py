from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Roadmap, RoadmapTask
from .services import DashboardService

@login_required
def dashboard_view(request):
    stats = DashboardService.get_statistics()
    # For now, just show the most recent active roadmaps for the dashboard
    recent_roadmaps = Roadmap.objects.filter(status='ACTIVE').order_by('-created_at')[:5]
    
    return render(request, 'roadmaps/dashboard.html', {
        'stats': stats,
        'recent_roadmaps': recent_roadmaps
    })

@login_required
def roadmap_detail_view(request, roadmap_id):
    roadmap = get_object_or_404(Roadmap, id=roadmap_id)
    # Group tasks by phase for template display
    tasks = roadmap.tasks.all().prefetch_related('dependencies')
    
    phases = {}
    for task in tasks:
        if task.phase not in phases:
            phases[task.phase] = []
        phases[task.phase].append(task)
        
    return render(request, 'roadmaps/roadmap_detail.html', {
        'roadmap': roadmap,
        'phases': phases
    })

@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(RoadmapTask, id=task_id)
    return render(request, 'roadmaps/task_detail.html', {
        'task': task
    })

@login_required
def roadmap_history_view(request, idea_id):
    roadmaps = Roadmap.objects.filter(startup_idea_id=idea_id).order_by('-version')
    return render(request, 'roadmaps/roadmap_history.html', {
        'roadmaps': roadmaps,
        'idea_id': idea_id
    })
