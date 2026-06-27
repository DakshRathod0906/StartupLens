from .normalization import NormalizationService
from .deduplication import DeduplicationService
from .source_scoring import SourceScoringService
from .dashboard import DashboardService, ResearchStatistics
from .research import ResearchService

__all__ = [
    'NormalizationService',
    'DeduplicationService',
    'SourceScoringService',
    'DashboardService',
    'ResearchStatistics',
    'ResearchService',
]
