import re

class NormalizationService:
    @staticmethod
    def normalize_title(title: str) -> str:
        if not title:
            return ""
        # Remove special characters and extra spaces, convert to lowercase
        text = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()

    @staticmethod
    def normalize_text(text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
