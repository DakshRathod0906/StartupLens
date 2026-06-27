import hashlib
import logging
import time
from typing import Dict, Any, Optional

from ai.models import PromptTemplate, AIConversation, AIRequest
from ai.prompt_builder import PromptBuilder
from ai.response_parser import ResponseParser
from startup_ideas.models import StartupIdea

logger = logging.getLogger('ai')

class GeminiClient:
    """
    Shared client for interacting with the Gemini API (Google GenAI SDK).
    Ensures that all AI interactions are strictly logged and read-only.
    """
    
    def __init__(self, service_name: str, model_name: str = "gemini-2.5-flash"):
        self.service_name = service_name
        self.model_name = model_name
        # In a real app we'd initialize the google-genai client here
        # self.client = genai.Client(...)
        
    def generate(
        self, 
        startup_idea: StartupIdea, 
        template_name: str, 
        context: Dict[str, Any],
        conversation_title: str = "Analysis",
        parse_as_json: bool = False
    ) -> Any:
        """
        Executes a prompt template and returns the parsed response.
        """
        # Retrieve active template
        template = PromptTemplate.objects.filter(name=template_name, is_active=True).order_by('-created_at').first()
        if not template:
            logger.error(f"No active PromptTemplate found for '{template_name}'")
            raise ValueError(f"No active PromptTemplate found for {template_name}")

        logger.info(f"AI request: service={self.service_name}, template={template_name}, idea='{startup_idea.title}'")
            
        # Build prompt
        system_prompt, user_prompt = PromptBuilder.build(template, context)
        full_prompt_text = f"System: {system_prompt}\nUser: {user_prompt}"
        
        # Calculate hash for audit logging
        input_hash = hashlib.sha256(full_prompt_text.encode('utf-8')).hexdigest()
        
        # Get or create conversation
        conversation, _ = AIConversation.objects.get_or_create(
            startup_idea=startup_idea,
            title=conversation_title
        )
        
        # Log request initiation
        request_log = AIRequest.objects.create(
            conversation=conversation,
            prompt_template=template,
            service_name=self.service_name,
            model_name=self.model_name,
            input_hash=input_hash,
            status=AIRequest.StatusChoices.PENDING
        )
        
        start_time = time.time()
        
        try:
            # === MOCK API CALL ===
            # response = self.client.models.generate_content(...)
            # For Phase 10 implementation, we simulate the Gemini API
            raw_response = self._mock_api_call(template_name, parse_as_json)
            # =====================
            
            end_time = time.time()
            latency_ms = int((end_time - start_time) * 1000)
            
            # Simulated token count
            tokens_used = len(full_prompt_text) // 4 + len(raw_response) // 4
            
            # Update log
            request_log.response = raw_response
            request_log.tokens_used = tokens_used
            request_log.latency_ms = latency_ms
            request_log.status = AIRequest.StatusChoices.SUCCESS
            request_log.save()

            logger.info(f"AI response: service={self.service_name}, tokens={tokens_used}, latency={latency_ms}ms")
            
            # Parse output
            if parse_as_json:
                return ResponseParser.parse_json(raw_response)
            return ResponseParser.parse_markdown(raw_response)
            
        except Exception as e:
            end_time = time.time()
            request_log.latency_ms = int((end_time - start_time) * 1000)
            request_log.status = AIRequest.StatusChoices.FAILED
            request_log.response = str(e)
            request_log.save()
            logger.error(f"AI request failed: service={self.service_name}, error={e}")
            raise e
            
    def _mock_api_call(self, template_name: str, as_json: bool) -> str:
        """Mock Gemini response for testing pipeline."""
        if as_json:
            return '{"summary": "This is a highly promising startup idea based on the analysis.", "score": 85}'
        return "This is a detailed mock AI commentary on the startup's viability."
