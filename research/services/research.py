from django.utils import timezone
import logging
from ..models import ResearchJob, ResearchSource
from ..constants import ResearchJobStatus, ResearchSourceStatus, ResearchProvider
from .normalization import NormalizationService
from .deduplication import DeduplicationService
from .source_scoring import SourceScoringService
from ..adapters.google import GoogleAdapter
# In reality we would dynamically instantiate adapters based on config.
# For Phase 3, we'll just run GoogleAdapter as an example.

logger = logging.getLogger(__name__)

class ResearchService:
    @staticmethod
    def execute_job(job: ResearchJob):
        job.status = ResearchJobStatus.RUNNING
        job.started_at = timezone.now()
        job.save(update_fields=['status', 'started_at'])
        
        adapters_to_run = [
            (ResearchProvider.GOOGLE, GoogleAdapter()),
        ]
        
        try:
            for provider, adapter in adapters_to_run:
                # 1. Search (Fetch raw data)
                raw_results = adapter.search(job.startup_idea.title)
                
                for raw in raw_results:
                    job.total_sources += 1
                    
                    try:
                        # 2. Parse
                        parsed_data = adapter.parse(raw)
                        
                        # 3. Normalization
                        canonical_url = NormalizationService.canonicalize_url(parsed_data['original_url'])
                        content_hash = NormalizationService.generate_content_hash(parsed_data['excerpt'])
                        
                        # 4. Deduplication
                        if DeduplicationService.is_duplicate(job.id, canonical_url, content_hash):
                            job.duplicate_sources += 1
                            continue
                            
                        # 5. Scoring
                        score = SourceScoringService.calculate_score(provider, parsed_data['domain'])
                        
                        # 6. Repository/Database
                        ResearchSource.objects.create(
                            research_job=job,
                            title=parsed_data['title'],
                            original_url=parsed_data['original_url'],
                            canonical_url=canonical_url,
                            domain=parsed_data['domain'],
                            provider=provider,
                            status=ResearchSourceStatus.NORMALIZED,
                            excerpt=parsed_data['excerpt'],
                            author=parsed_data['author'],
                            published_at=parsed_data.get('published_at'),
                            credibility_score=score,
                            content_hash=content_hash,
                            metadata=parsed_data['metadata']
                        )
                        job.processed_sources += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to process source for job {job.id}: {e}")
                        job.failed_sources += 1
            
            job.status = ResearchJobStatus.COMPLETED
            
        except Exception as e:
            job.status = ResearchJobStatus.FAILED
            job.error_message = str(e)
            
        finally:
            job.completed_at = timezone.now()
            if job.started_at:
                job.duration = int((job.completed_at - job.started_at).total_seconds())
            job.save()
