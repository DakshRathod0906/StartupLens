from django.contrib import admin
from ai.models import PromptTemplate, AIConversation, AIRequest


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'startup_idea', 'created_at')
    search_fields = ('title',)


@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'model_name', 'status', 'tokens_used', 'latency_ms', 'created_at')
    list_filter = ('status', 'service_name', 'model_name')
    readonly_fields = ('input_hash', 'response')
