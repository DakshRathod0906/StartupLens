from typing import Dict, Any
from ai.models import PromptTemplate

class PromptBuilder:
    """
    Constructs concrete prompts by injecting dynamic context into PromptTemplates.
    """
    
    @staticmethod
    def build(template: PromptTemplate, context: Dict[str, Any]) -> tuple[str, str]:
        """
        Takes a PromptTemplate and context dictionary, and returns the formatted 
        system and user prompts.
        
        Args:
            template: The PromptTemplate instance.
            context: Dictionary of variables to inject into the template.
            
        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        # In a real app we might use Jinja2 or Django templates for prompt formatting.
        # For this implementation, we use standard python string formatting.
        try:
            formatted_system = template.system_prompt.format(**context)
        except KeyError:
            # Fallback if formatting fails due to missing keys
            formatted_system = template.system_prompt
            
        try:
            formatted_user = template.user_prompt.format(**context)
        except KeyError:
            formatted_user = template.user_prompt
            
        return formatted_system, formatted_user
