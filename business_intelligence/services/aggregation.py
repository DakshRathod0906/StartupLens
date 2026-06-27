import logging
from decimal import Decimal
from django.db import transaction
from startup_ideas.models import StartupIdea
from research.models import ResearchJob
from knowledge.models import Finding
from ..models import Insight
from ..constants import InsightStatus
from ..aggregators import ALL_AGGREGATORS
from .normalization import NormalizationService
from .confidence import ConfidenceService

logger = logging.getLogger(__name__)

class AggregationService:
    @staticmethod
    def aggregate_for_job(job: ResearchJob):
        """
        Coordinates the aggregation pipeline for a given job.
        Finds all findings for this job's idea and aggregates them.
        """
        idea = job.startup_idea
        
        # Mark all old insights as STALE
        Insight.objects.filter(startup_idea=idea).update(status=InsightStatus.STALE)
        
        # Load findings for this idea
        all_findings = list(Finding.objects.filter(startup_idea=idea))
        
        for aggregator in ALL_AGGREGATORS:
            try:
                # Filter findings the aggregator supports
                supported_findings = [f for f in all_findings if aggregator.supports(f.finding_type)]
                
                # Get raw insights
                raw_insights = aggregator.aggregate(idea, supported_findings)
                
                for raw in raw_insights:
                    title = NormalizationService.normalize_name(raw.get('title', ''))
                    
                    # Calculate version if this insight title already existed for this idea
                    last_version = Insight.objects.filter(
                        startup_idea=idea,
                        insight_type=raw.get('insight_type'),
                        title=title
                    ).order_by('-version').first()
                    
                    next_version = 1
                    if last_version:
                        next_version = last_version.version + 1
                    
                    with transaction.atomic():
                        insight = Insight.objects.create(
                            startup_idea=idea,
                            generated_from_job=job,
                            insight_type=raw.get('insight_type'),
                            status=InsightStatus.GENERATED,
                            title=title,
                            summary=raw.get('summary', ''),
                            confidence_score=raw.get('confidence_score', Decimal('0.5')),
                            version=next_version,
                            metadata=raw.get('metadata', {})
                        )
                        
                        supporting_ids = raw.get('supporting_finding_ids', [])
                        if supporting_ids:
                            insight.supporting_findings.add(*supporting_ids)
            except Exception as e:
                logger.error(f"Aggregator {aggregator.name} failed for idea {idea.id}: {e}")
