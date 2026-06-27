from dataclasses import dataclass
from decimal import Decimal
from django.db.models import Avg, Sum
from ..models import ResearchJob, ResearchSource
from ..constants import ResearchJobStatus

@dataclass
class ResearchStatistics:
    total_jobs: int
    running_jobs: int
    completed_jobs: int
    failed_jobs: int
    total_sources: int
    duplicate_sources: int
    average_score: Decimal

class DashboardService:
    @staticmethod
    def get_statistics() -> ResearchStatistics:
        jobs = ResearchJob.objects.all()
        
        total_jobs = jobs.count()
        running_jobs = jobs.filter(status=ResearchJobStatus.RUNNING).count()
        completed_jobs = jobs.filter(status=ResearchJobStatus.COMPLETED).count()
        failed_jobs = jobs.filter(status=ResearchJobStatus.FAILED).count()
        
        aggregates = jobs.aggregate(
            total=Sum('total_sources'),
            duplicates=Sum('duplicate_sources')
        )
        
        total_sources = aggregates['total'] or 0
        duplicate_sources = aggregates['duplicates'] or 0
        
        avg_score_dict = ResearchSource.objects.aggregate(avg=Avg('credibility_score'))
        avg_score = Decimal(avg_score_dict['avg'] or 0).quantize(Decimal('0.01'))
        
        return ResearchStatistics(
            total_jobs=total_jobs,
            running_jobs=running_jobs,
            completed_jobs=completed_jobs,
            failed_jobs=failed_jobs,
            total_sources=total_sources,
            duplicate_sources=duplicate_sources,
            average_score=avg_score
        )
