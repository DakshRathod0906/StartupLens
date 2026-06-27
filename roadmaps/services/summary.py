from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from ..models import Roadmap, RoadmapTask
from ..constants import RoadmapTaskStatus
from recommendations.constants import RecommendationPriority

class SummaryService:
    @staticmethod
    def generate_summary(roadmap: Roadmap):
        tasks = RoadmapTask.objects.filter(roadmap=roadmap)
        
        total = tasks.count()
        completed = tasks.filter(status=RoadmapTaskStatus.COMPLETED).count()
        blocked = tasks.filter(status=RoadmapTaskStatus.BLOCKED).count()
        critical = tasks.filter(priority=RecommendationPriority.CRITICAL).count()
        
        # Calculate duration
        duration_agg = tasks.aggregate(Sum('estimated_days'))
        overall_duration = duration_agg['estimated_days__sum'] or 0
        
        # Calculate completion percentage
        completion_pct = 0.00
        if total > 0:
            completion_pct = round((completed / total) * 100, 2)
            
        estimated_completion = timezone.now().date() + timedelta(days=overall_duration)
        
        # Determine summary string
        summary_text = f"Roadmap generated with {total} total tasks over an estimated {overall_duration} days."
        
        roadmap.total_tasks = total
        roadmap.completed_tasks = completed
        roadmap.blocked_tasks = blocked
        roadmap.critical_tasks = critical
        roadmap.completion_percentage = completion_pct
        roadmap.overall_duration_days = overall_duration
        roadmap.estimated_completion = estimated_completion
        roadmap.summary = summary_text
        roadmap.save()
