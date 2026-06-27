from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAdapter(ABC):
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    def fetch(self, url: str) -> str:
        pass
        
    @abstractmethod
    def parse(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes raw API data and parses it into the standard format:
        {
            "title": str,
            "original_url": str,
            "domain": str,
            "excerpt": str,
            "author": str,
            "published_at": str (iso format),
            "metadata": dict
        }
        """
        pass
