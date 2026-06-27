from django.contrib import admin
from emails.models import NotificationPreference, NotificationTemplate, NotificationQueue, EmailLog

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'analysis_complete', 'weekly_summary', 'marketing', 'investor_matches')

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')

@admin.register(NotificationQueue)
class NotificationQueueAdmin(admin.ModelAdmin):
    list_display = ('template', 'recipient', 'status', 'scheduled_at', 'sent_at')
    list_filter = ('status',)

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('recipient_email', 'subject', 'status', 'sent_at')
    list_filter = ('status',)
