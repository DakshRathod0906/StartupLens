from typing import List, Dict, Any
from .base import BaseExtractor
from research.models import ResearchSource

class CompetitorExtractor(BaseExtractor):
    @property
    def name(self) -> str:
        return "CompetitorExtractor"

    def supports(self, source: ResearchSource) -> bool:
        # Mock logic: if snippet has 'competitor' or similar
        text = (source.title + " " + source.excerpt).lower()
        return "startup" in text or "competitor" in text or "company" in text

    def extract(self, source: ResearchSource) -> List[Dict[str, Any]]:
        # Mock deterministic extraction based on some simple keyword
        findings = []
        text = source.excerpt.lower()
        if "chatgpt" in text:
            findings.append({
                "raw_title": "ChatGPT",
                "raw_description": "AI conversational model developed by OpenAI.",
                "raw_confidence": 0.90,
                "metadata": {"paragraph": 1}
            })
        if not findings:
            # Fallback mock finding
            findings.append({
                "raw_title": "Generic Competitor",
                "raw_description": "A startup working in a similar space.",
                "raw_confidence": 0.50,
                "metadata": {"paragraph": 1}
            })
        return findings
