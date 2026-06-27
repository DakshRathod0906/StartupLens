import re

class NormalizationService:
    @staticmethod
    def normalize_name(name: str) -> str:
        if not name:
            return ""
        text = re.sub(r'[^a-zA-Z0-9\s]', '', name)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().title()
