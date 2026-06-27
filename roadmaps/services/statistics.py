from django.db.models import Count
from ..models import Roadmap, RoadmapTask

class StatisticsService:
    @staticmethod
    def get_phase_counts(roadmap: Roadmap):
        return RoadmapTask.objects.filter(roadmap=roadmap).values('phase').annotate(count=Count('id'))
