import json
import os
from django.conf import settings
from typing import List, Dict, Any
from .base import BaseAdapter

class GoogleAdapter(BaseAdapter):
    def __init__(self):
        self.fixture_path = os.path.join(
            settings.BASE_DIR, 'research', 'fixtures', 'google', 'search.json'
        )

    def search(self, query: str) -> List[Dict[str, Any]]:
        if os.path.exists(self.fixture_path):
            with open(self.fixture_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def fetch(self, url: str) -> str:
        # For mock, we just return a stub
        return "Mock fetched content for Google."

    def parse(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": raw_data.get("title", ""),
            "original_url": raw_data.get("link", ""),
            "domain": raw_data.get("domain", ""),
            "excerpt": raw_data.get("snippet", ""),
            "author": raw_data.get("author", ""),
            "published_at": raw_data.get("published_date", None),
            "metadata": {
                "source": "google_search"
            }
        }
