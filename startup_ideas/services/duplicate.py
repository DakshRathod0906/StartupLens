from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import re
from ..models import StartupIdea

class DuplicateConfidence(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EXACT = "EXACT"

@dataclass
class DuplicateCheckResult:
    is_duplicate: bool
    confidence: DuplicateConfidence
    similar_ideas: List[StartupIdea]

class DuplicateDetectionService:
    @staticmethod
    def normalize_title(title: str) -> str:
        """
        Normalizes a title for comparison:
        lowercase, remove special characters, replace multiple spaces with single space.
        """
        # Convert to lowercase
        normalized = title.lower()
        # Remove non-alphanumeric (keep spaces)
        normalized = re.sub(r'[^a-z0-9\s]', ' ', normalized)
        # Condense multiple spaces to single space
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized

    @classmethod
    def check_duplicate(cls, owner, title: str, exclude_id: Optional[int] = None) -> DuplicateCheckResult:
        normalized_new_title = cls.normalize_title(title)
        
        # We only check against ideas owned by the same user to prevent self-duplication
        qs = StartupIdea.objects.owned_by(owner)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
            
        similar_ideas = []
        highest_confidence = DuplicateConfidence.LOW
        is_duplicate = False
        
        for idea in qs:
            normalized_existing = cls.normalize_title(idea.title)
            
            if normalized_existing == normalized_new_title:
                similar_ideas.append(idea)
                is_duplicate = True
                highest_confidence = DuplicateConfidence.EXACT
            elif normalized_new_title in normalized_existing or normalized_existing in normalized_new_title:
                # E.g. "Resume Builder" vs "AI Resume Builder"
                # This is a weak check, but better than nothing without full NLP/AI
                if len(normalized_existing) > 5 and len(normalized_new_title) > 5:
                    similar_ideas.append(idea)
                    if not is_duplicate:
                        is_duplicate = True
                        highest_confidence = DuplicateConfidence.HIGH
                        
        return DuplicateCheckResult(
            is_duplicate=is_duplicate,
            confidence=highest_confidence,
            similar_ideas=similar_ideas
        )
