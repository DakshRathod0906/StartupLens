import logging
from research.models import ResearchSource
from ..models import Finding
from ..constants import ProcessingStatus
from ..extractors import ALL_EXTRACTORS
from .classification import ClassificationService
from .normalization import NormalizationService
from .confidence import ConfidenceService
from .deduplication import DeduplicationService

logger = logging.getLogger(__name__)

class ExtractionService:
    @staticmethod
    def process_source(source: ResearchSource):
        """
        Coordinates the extraction pipeline for a given source.
        """
        for extractor in ALL_EXTRACTORS:
            if not extractor.supports(source):
                continue
                
            try:
                raw_findings = extractor.extract(source)
                
                for raw in raw_findings:
                    title = NormalizationService.normalize_text(raw.get('raw_title', ''))
                    normalized_title = NormalizationService.normalize_title(title)
                    description = NormalizationService.normalize_text(raw.get('raw_description', ''))
                    
                    finding_type = ClassificationService.classify(
                        title=title,
                        description=description,
                        extractor_name=extractor.name
                    )
                    
                    if DeduplicationService.is_duplicate(source.id, finding_type, normalized_title):
                        continue
                        
                    confidence = ConfidenceService.calculate_confidence(
                        source=source,
                        raw_confidence=raw.get('raw_confidence', 0.5)
                    )
                    
                    Finding.objects.create(
                        research_source=source,
                        startup_idea=source.research_job.startup_idea,
                        finding_type=finding_type,
                        title=title,
                        normalized_title=normalized_title,
                        description=description,
                        extractor_name=extractor.name,
                        processing_status=ProcessingStatus.EXTRACTED,
                        confidence_score=confidence,
                        metadata=raw.get('metadata', {})
                    )
                    
            except Exception as e:
                logger.error(f"Extractor {extractor.name} failed on source {source.id}: {e}")
                # We could create a FAILED finding here if desired for visibility
                Finding.objects.create(
                    research_source=source,
                    startup_idea=source.research_job.startup_idea,
                    finding_type="OTHER",
                    title=f"Failed Extraction: {extractor.name}",
                    normalized_title=f"failed_{extractor.name.lower()}",
                    description=str(e),
                    extractor_name=extractor.name,
                    processing_status=ProcessingStatus.FAILED,
                    confidence_score=0.0
                )
