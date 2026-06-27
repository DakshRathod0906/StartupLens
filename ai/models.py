import uuid
from django.db import models
from startup_ideas.models import StartupIdea

class PromptTemplate(models.Model):
    """
    First-class entity for AI prompts to decouple them from code and guarantee reproducibility.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    system_prompt = models.TextField()
    user_prompt = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'version')

    def __str__(self):
        return f"{self.name} (v{self.version})"


class AIConversation(models.Model):
    """
    Groups AI requests into a conversation to support multi-turn chats.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startup_idea = models.ForeignKey(StartupIdea, on_delete=models.CASCADE, related_name="ai_conversations")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AI Conversation for {self.startup_idea.title}: {self.title}"


class AIRequest(models.Model):
    """
    Strict audit log of AI interactions. AI services are strictly read-only.
    """
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name="requests")
    prompt_template = models.ForeignKey(PromptTemplate, on_delete=models.PROTECT, null=True, blank=True)
    service_name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    input_hash = models.CharField(max_length=64, help_text="SHA-256 of the actual prompt text sent")
    response = models.TextField(blank=True)
    tokens_used = models.PositiveIntegerField(default=0)
    latency_ms = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.PENDING
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_name} request on {self.created_at}"
