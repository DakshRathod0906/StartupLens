from dataclasses import dataclass
from ..models import Roadmap, RoadmapStatus

@dataclass
class RoadmapStatistics:
    total_tasks: int
    completed: int
    blocked: int
    critical: int
    completion_percentage: float
    remaining_days: int
    graph_depth: int = 0
    critical_path_length: int = 0
    average_dependency_count: float = 0.0
    leaf_tasks: int = 0

class DashboardService:
    @staticmethod
    def get_statistics() -> RoadmapStatistics:
        active_roadmaps = Roadmap.objects.filter(status=RoadmapStatus.ACTIVE)
        
        total_tasks = sum(r.total_tasks for r in active_roadmaps)
        completed = sum(r.completed_tasks for r in active_roadmaps)
        blocked = sum(r.blocked_tasks for r in active_roadmaps)
        critical = sum(r.critical_tasks for r in active_roadmaps)
        
        # Calculate overall completion percentage and remaining days
        total_days = sum(r.overall_duration_days for r in active_roadmaps)
        remaining_days = total_days # Simplification for now
        
        completion_pct = 0.0
        if total_tasks > 0:
            completion_pct = round((completed / total_tasks) * 100, 2)
            
        return RoadmapStatistics(
            total_tasks=total_tasks,
            completed=completed,
            blocked=blocked,
            critical=critical,
            completion_percentage=completion_pct,
            remaining_days=remaining_days
        )
