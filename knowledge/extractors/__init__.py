from .base import BaseExtractor
from .competitor import CompetitorExtractor

# In a real scenario we'd list all of them
ALL_EXTRACTORS = [
    CompetitorExtractor(),
]
