import hashlib
import io
import logging
from django.core.files.base import ContentFile
from reports.models import Report, ReportTemplate
from evaluation.models import EvaluationSnapshot

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

logger = logging.getLogger('reports')


class ReportGenerationService:
    """
    Generates deterministic PDF reports directly from an EvaluationSnapshot.
    Reports are always generated from immutable snapshot data.
    """

    @staticmethod
    def generate_executive_report(snapshot_id: str, generated_by_id: str = None) -> Report:
        """
        Generates an executive report for the given evaluation snapshot.
        """
        logger.info(f"Starting report generation for snapshot_id={snapshot_id}")
        snapshot = EvaluationSnapshot.objects.select_related(
            'final_evaluation__startup_idea__owner',
            'final_evaluation__startup_idea__industry',
        ).get(id=snapshot_id)

        template, _ = ReportTemplate.objects.get_or_create(
            name="Default Executive Report",
            defaults={"version": "1.0"}
        )

        report = Report.objects.create(
            evaluation_snapshot=snapshot,
            report_template=template,
            generated_by_id=generated_by_id,
            status=Report.StatusChoices.GENERATING,
        )

        try:
            pdf_bytes = ReportGenerationService._build_pdf(snapshot)

            checksum = hashlib.sha256(pdf_bytes).hexdigest()

            idea = snapshot.final_evaluation.startup_idea
            filename = f"startup_report_{idea.id}_v{snapshot.final_evaluation.version}.pdf"
            report.file_path.save(filename, ContentFile(pdf_bytes))
            report.checksum = checksum
            report.status = Report.StatusChoices.COMPLETED
            report.save(update_fields=['checksum', 'status', 'file_path'])
            logger.info(f"Report generated: id={report.id}, checksum={checksum[:16]}..., size={len(pdf_bytes)} bytes")
            return report

        except Exception as e:
            report.status = Report.StatusChoices.FAILED
            report.save(update_fields=['status'])
            logger.error(f"Report generation failed for snapshot_id={snapshot_id}: {e}")
            raise

    @staticmethod
    def _build_pdf(snapshot: EvaluationSnapshot) -> bytes:
        """
        Builds the PDF document using ReportLab.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                topMargin=0.75 * inch, bottomMargin=0.75 * inch)
        styles = getSampleStyleSheet()
        story = []

        evaluation = snapshot.final_evaluation
        idea = evaluation.startup_idea

        # ── Title ──
        story.append(Paragraph("StartupLens Executive Report", styles['Title']))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563eb")))
        story.append(Spacer(1, 18))

        # ── Startup Info ──
        story.append(Paragraph(f"Startup Idea: {idea.title}", styles['Heading2']))
        story.append(Paragraph(f"Stage: {idea.get_startup_stage_display()}", styles['Normal']))
        story.append(Paragraph(f"Owner: {idea.owner.get_full_name() or idea.owner.username}", styles['Normal']))
        story.append(Spacer(1, 12))

        # ── Overall Score ──
        story.append(Paragraph("Overall Assessment", styles['Heading3']))
        score_data = [
            ["Metric", "Value"],
            ["Score", f"{snapshot.overall_score_snapshot}/100"],
            ["Grade", snapshot.overall_grade_snapshot],
            ["Readiness", evaluation.get_readiness_level_display()],
            ["Confidence", f"{evaluation.confidence_score}%"],
        ]
        score_table = Table(score_data, colWidths=[2.5 * inch, 3 * inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2563eb")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 18))

        # ── Assessment Breakdown ──
        assessment = snapshot.assessment_snapshot
        if assessment and isinstance(assessment, dict):
            story.append(Paragraph("Assessment Breakdown", styles['Heading3']))
            for key, value in assessment.items():
                story.append(Paragraph(f"• {key}: {value}", styles['Normal']))
            story.append(Spacer(1, 12))

        # ── Key Strengths ──
        strengths = snapshot.strength_snapshot
        if strengths and isinstance(strengths, list):
            story.append(Paragraph("Key Strengths", styles['Heading3']))
            for s in strengths:
                story.append(Paragraph(f"✓ {s}", styles['Normal']))
            story.append(Spacer(1, 12))

        # ── Key Risks ──
        risks = snapshot.risk_snapshot
        if risks and isinstance(risks, list):
            story.append(Paragraph("Key Risks", styles['Heading3']))
            for r in risks:
                story.append(Paragraph(f"⚠ {r}", styles['Normal']))
            story.append(Spacer(1, 12))

        # ── Recommendations ──
        recs = snapshot.recommendation_snapshot
        if recs and isinstance(recs, dict):
            story.append(Paragraph("Recommendations", styles['Heading3']))
            story.append(Paragraph(f"Total: {recs.get('total_recommendations', 0)}", styles['Normal']))
            story.append(Paragraph(f"Critical: {recs.get('critical_count', 0)}", styles['Normal']))
            story.append(Spacer(1, 12))

        # ── Roadmap ──
        roadmap = snapshot.roadmap_snapshot
        if roadmap and isinstance(roadmap, dict):
            story.append(Paragraph("Execution Roadmap", styles['Heading3']))
            story.append(Paragraph(f"Duration: {roadmap.get('overall_duration_days', 'N/A')} days", styles['Normal']))
            story.append(Paragraph(f"Total Tasks: {roadmap.get('total_tasks', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 12))

        # ── Executive Summary ──
        summary = snapshot.summary_snapshot
        if summary and isinstance(summary, dict):
            story.append(Paragraph("Executive Summary", styles['Heading3']))
            story.append(Paragraph(str(summary.get('executive_summary', '')), styles['Normal']))

        doc.build(story)
        return buffer.getvalue()
