import json
from typing import Dict, Any

class ResponseParser:
    """
    Parses unstructured or semi-structured AI responses into structured data.
    """
    
    @staticmethod
    def parse_json(raw_response: str) -> Dict[str, Any]:
        """
        Extracts and parses JSON from an LLM response. 
        Handles cases where the LLM wraps the response in markdown code blocks.
        """
        text = raw_response.strip()
        
        # Remove markdown code block formatting if present
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
            
        if text.endswith("```"):
            text = text[:-3]
            
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # Fallback or error handling
            raise ValueError(f"Failed to parse AI response as JSON: {e}\nRaw: {raw_response}")
            
    @staticmethod
    def parse_markdown(raw_response: str) -> str:
        """
        Cleans up raw markdown text.
        """
        return raw_response.strip()
