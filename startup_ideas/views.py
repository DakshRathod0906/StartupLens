from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse

from .models import StartupIdea
from .forms import StartupIdeaForm, SearchForm
from .mixins import OwnerRequiredMixin
from .services.create import CreateService
from .services.update import UpdateService
from .services.archive import ArchiveService
from .services.restore import RestoreService
from .services.delete import DeleteService
from .services.duplicate import DuplicateDetectionService, DuplicateConfidence
from .services.search import SearchService, IdeaSearchFilter
from .services.dashboard import DashboardService
from .exceptions import VersionConflictError, DuplicateIdeaError

@login_required
def dashboard_view(request):
    metrics = DashboardService.get_dashboard_data(request.user)
    return render(request, 'startup_ideas/dashboard.html', {'metrics': metrics})

@login_required
def idea_list_view(request):
    form = SearchForm(request.GET)
    filters = IdeaSearchFilter(owner=request.user)
    
    if form.is_valid():
        filters.keyword = form.cleaned_data.get('keyword')
        industry = form.cleaned_data.get('industry')
        filters.industry_id = industry.id if industry else None
        filters.status = form.cleaned_data.get('status')
        filters.stage = form.cleaned_data.get('stage')
        
    qs = SearchService.search(filters)
    
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'startup_ideas/list.html', {'form': form, 'page_obj': page_obj})

@login_required
def idea_create_view(request):
    if request.method == 'POST':
        form = StartupIdeaForm(request.POST)
        if form.is_valid():
            # Check for duplicates first if it wasn't confirmed
            ignore_duplicate = request.POST.get('ignore_duplicate') == 'true'
            title = form.cleaned_data.get('title')
            
            duplicate_result = DuplicateDetectionService.check_duplicate(request.user, title)
            
            if duplicate_result.is_duplicate and duplicate_result.confidence in [DuplicateConfidence.HIGH, DuplicateConfidence.EXACT] and not ignore_duplicate:
                return render(request, 'startup_ideas/create.html', {
                    'form': form,
                    'duplicate_warning': True,
                    'similar_ideas': duplicate_result.similar_ideas
                })
            
            # Create
            idea = CreateService.create_idea(request.user, form.cleaned_data)
            messages.success(request, "Startup idea created successfully.")
            return redirect('startup_ideas:detail', slug=idea.slug)
    else:
        form = StartupIdeaForm()
        
    return render(request, 'startup_ideas/create.html', {'form': form})

@login_required
def idea_detail_view(request, slug):
    idea = get_object_or_404(StartupIdea, slug=slug, owner=request.user)
    return render(request, 'startup_ideas/detail.html', {'idea': idea})

@login_required
def idea_edit_view(request, slug):
    idea = get_object_or_404(StartupIdea, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        form = StartupIdeaForm(request.POST, instance=idea)
        if form.is_valid():
            try:
                submitted_version = int(request.POST.get('version', idea.version))
                UpdateService.update_idea(request.user, idea, form.cleaned_data, submitted_version)
                messages.success(request, "Startup idea updated successfully.")
                return redirect('startup_ideas:detail', slug=idea.slug)
            except VersionConflictError as e:
                messages.error(request, str(e))
                # Re-render with new version so they can try again, or let them refresh
                idea.refresh_from_db()
                form = StartupIdeaForm(instance=idea)
    else:
        form = StartupIdeaForm(instance=idea)
        
    return render(request, 'startup_ideas/edit.html', {'form': form, 'idea': idea})

@login_required
def idea_archive_view(request, slug):
    idea = get_object_or_404(StartupIdea, slug=slug, owner=request.user)
    if request.method == 'POST':
        ArchiveService.archive_idea(request.user, idea)
        messages.success(request, "Startup idea archived.")
        return redirect('startup_ideas:detail', slug=idea.slug)
    return render(request, 'startup_ideas/archive_confirm.html', {'idea': idea})

@login_required
def idea_restore_view(request, slug):
    idea = get_object_or_404(StartupIdea, slug=slug, owner=request.user)
    if request.method == 'POST':
        RestoreService.restore_idea(request.user, idea)
        messages.success(request, "Startup idea restored.")
        return redirect('startup_ideas:detail', slug=idea.slug)
    return redirect('startup_ideas:detail', slug=idea.slug)

@login_required
def idea_delete_view(request, slug):
    idea = get_object_or_404(StartupIdea, slug=slug, owner=request.user)
    if request.method == 'POST':
        DeleteService.soft_delete_idea(request.user, idea)
        messages.success(request, "Startup idea deleted.")
        return redirect('startup_ideas:list')
    return render(request, 'startup_ideas/delete_confirm.html', {'idea': idea})
