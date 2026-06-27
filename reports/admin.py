from django.contrib import admin
from reports.models import ReportTemplate, ReportSection, Report

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'is_active', 'created_at')
    list_filter = ('is_active',)

@admin.register(ReportSection)
class ReportSectionAdmin(admin.ModelAdmin):
    list_display = ('template', 'title', 'order', 'content_type', 'is_active')
    list_filter = ('template', 'content_type', 'is_active')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'evaluation_snapshot', 'status', 'version', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('checksum',)
