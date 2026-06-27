import hashlib
from urllib.parse import urlparse, urlunparse
import re

class NormalizationService:
    @staticmethod
    def clean_text(text: str) -> str:
        """Removes extra whitespace and newlines."""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    @staticmethod
    def generate_content_hash(text: str) -> str:
        """Generates a deterministic SHA-256 hash of the cleaned content."""
        cleaned = NormalizationService.clean_text(text)
        return hashlib.sha256(cleaned.encode('utf-8')).hexdigest()
        
    @staticmethod
    def canonicalize_url(url: str) -> str:
        """Strips fragments and common tracking parameters from a URL."""
        if not url:
            return ""
            
        parsed = urlparse(url)
        # Remove tracking parameters
        query = parsed.query
        if query:
            params = []
            for pair in query.split('&'):
                if not pair:
                    continue
                key = pair.split('=')[0].lower()
                if not key.startswith('utm_') and key not in ['fbclid', 'gclid', 'ref']:
                    params.append(pair)
            query = '&'.join(params)
            
        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            query,
            "" # Strip fragment
        )).rstrip('/')
