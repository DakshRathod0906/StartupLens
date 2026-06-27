from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import FileResponse

from authentication.models import User, UserLoginHistory
from startup_ideas.models import StartupIdea, Tag, Industry
from research.models import ResearchJob, ResearchSource
from knowledge.models import Finding
from business_intelligence.models import Insight
from assessment.models import AssessmentRule, Assessment, OverallAssessment
from recommendations.models import RecommendationRule, Recommendation, RecommendationSummary
from roadmaps.models import TaskTemplate, Roadmap, RoadmapTask
from evaluation.models import FinalEvaluation, EvaluationSnapshot
from reports.models import ReportTemplate, Report
from emails.models import NotificationPreference, EmailLog
from investors.models import Investor, StartupInvestorMatch
from ai.models import PromptTemplate, AIConversation, AIRequest
from ml.models import PredictionModel, PredictionResult, StartupFeatureVector

from api.serializers import (
    UserSerializer, UserLoginHistorySerializer,
    StartupIdeaListSerializer, StartupIdeaDetailSerializer, StartupIdeaWriteSerializer,
    TagSerializer, IndustrySerializer,
    ResearchJobSerializer, ResearchSourceSerializer,
    FindingSerializer,
    InsightSerializer,
    AssessmentRuleSerializer, AssessmentSerializer, OverallAssessmentSerializer,
    RecommendationRuleSerializer, RecommendationSerializer, RecommendationSummarySerializer,
    RoadmapSerializer, RoadmapTaskSerializer,
    FinalEvaluationSerializer, EvaluationSnapshotSerializer,
    ReportTemplateSerializer, ReportSerializer,
    NotificationPreferenceSerializer, EmailLogSerializer,
    InvestorSerializer, StartupInvestorMatchSerializer,
    PromptTemplateSerializer, AIConversationSerializer, AIRequestSerializer,
    PredictionModelSerializer, PredictionResultSerializer, StartupFeatureVectorSerializer,
)

from reports.services.generation import ReportGenerationService
from investors.services.matching import InvestorMatchingService


# ─── Authentication ───────────────────────────────────────────────

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User profiles. Read-only for non-admin users."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class UserLoginHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserLoginHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserLoginHistory.objects.filter(user=self.request.user).select_related('user')


# ─── Startup Ideas ────────────────────────────────────────────────

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class StartupIdeaViewSet(viewsets.ModelViewSet):
    """Full CRUD for startup ideas owned by the authenticated user."""
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'short_description', 'problem_statement']
    ordering_fields = ['created_at', 'updated_at', 'title', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        return StartupIdea.objects.filter(
            owner=self.request.user
        ).select_related('owner', 'industry').prefetch_related('tags')

    def get_serializer_class(self):
        if self.action == 'list':
            return StartupIdeaListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return StartupIdeaWriteSerializer
        return StartupIdeaDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ─── Research ─────────────────────────────────────────────────────

class ResearchJobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResearchJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ResearchJob.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea').prefetch_related('sources').order_by('-created_at')


class ResearchSourceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResearchSourceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'domain']
    ordering_fields = ['credibility_score', 'published_at']

    def get_queryset(self):
        return ResearchSource.objects.filter(
            research_job__startup_idea__owner=self.request.user
        ).select_related('research_job')


# ─── Knowledge ────────────────────────────────────────────────────

class FindingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FindingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['confidence_score', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Finding.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea', 'research_source')


# ─── Business Intelligence ────────────────────────────────────────

class InsightViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InsightSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'summary']
    ordering_fields = ['confidence_score', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Insight.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea', 'generated_from_job')


# ─── Assessment ───────────────────────────────────────────────────

class AssessmentRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssessmentRule.objects.filter(is_active=True).order_by('assessment_type')
    serializer_class = AssessmentRuleSerializer
    permission_classes = [IsAuthenticated]


class AssessmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['percentage', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Assessment.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea')


class OverallAssessmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OverallAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OverallAssessment.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea')


# ─── Recommendations ─────────────────────────────────────────────

class RecommendationRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecommendationRule.objects.filter(is_active=True)
    serializer_class = RecommendationRuleSerializer
    permission_classes = [IsAuthenticated]


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Recommendation.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea', 'assessment', 'matched_rule')


class RecommendationSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecommendationSummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecommendationSummary.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea')


# ─── Roadmaps ─────────────────────────────────────────────────────

class RoadmapViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoadmapSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Roadmap.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea', 'progress').prefetch_related('tasks').order_by('-created_at')


class RoadmapTaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoadmapTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['phase', 'dependency_level', 'execution_order', 'priority']

    def get_queryset(self):
        return RoadmapTask.objects.filter(
            roadmap__startup_idea__owner=self.request.user
        ).select_related('roadmap', 'recommendation', 'task_template')


# ─── Evaluation ───────────────────────────────────────────────────

class FinalEvaluationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FinalEvaluationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FinalEvaluation.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related(
            'startup_idea', 'overall_assessment',
            'recommendation_summary', 'roadmap', 'snapshot'
        )


# ─── Reports ──────────────────────────────────────────────────────

class ReportTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReportTemplate.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ReportTemplateSerializer
    permission_classes = [IsAuthenticated]


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(
            generated_by=self.request.user
        ).select_related('evaluation_snapshot', 'report_template').order_by('-created_at')

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download the generated PDF report."""
        report = self.get_object()
        if report.status != Report.StatusChoices.COMPLETED or not report.file_path:
            return Response(
                {"success": False, "message": "Report is not ready for download."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return FileResponse(report.file_path.open('rb'), content_type='application/pdf')

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate a new PDF report from an evaluation snapshot."""
        snapshot_id = request.data.get('snapshot_id')
        if not snapshot_id:
            return Response(
                {"success": False, "message": "snapshot_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            report = ReportGenerationService.generate_executive_report(
                snapshot_id=snapshot_id,
                generated_by_id=str(request.user.id),
            )
            return Response(
                {"success": True, "message": "Report generated.", "data": ReportSerializer(report).data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ─── Email ────────────────────────────────────────────────────────

class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)


class EmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmailLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmailLog.objects.filter(recipient_email=self.request.user.email)


# ─── Investors ────────────────────────────────────────────────────

class InvestorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Investor.objects.filter(is_active=True).select_related('preferences').order_by('name')
    serializer_class = InvestorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class StartupInvestorMatchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StartupInvestorMatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StartupInvestorMatch.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea', 'investor', 'explanation')

    @action(detail=False, methods=['post'])
    def run_matching(self, request):
        """Run investor matching for a given startup idea."""
        idea_id = request.data.get('startup_idea_id')
        if not idea_id:
            return Response(
                {"success": False, "message": "startup_idea_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            idea = StartupIdea.objects.get(id=idea_id, owner=request.user)
            matches = InvestorMatchingService.match_startup(idea)
            return Response(
                {"success": True, "message": f"{len(matches)} matches found.",
                 "data": StartupInvestorMatchSerializer(matches, many=True).data},
                status=status.HTTP_200_OK,
            )
        except StartupIdea.DoesNotExist:
            return Response(
                {"success": False, "message": "Startup idea not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


# ─── AI ───────────────────────────────────────────────────────────

class PromptTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PromptTemplate.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = PromptTemplateSerializer
    permission_classes = [IsAuthenticated]


class AIConversationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AIConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIConversation.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea').prefetch_related('requests').order_by('-created_at')


class AIRequestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AIRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIRequest.objects.filter(
            conversation__startup_idea__owner=self.request.user
        ).select_related('conversation', 'prompt_template')


# ─── Machine Learning ────────────────────────────────────────────

class PredictionModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PredictionModel.objects.all().order_by('-created_at')
    serializer_class = PredictionModelSerializer
    permission_classes = [IsAuthenticated]


class PredictionResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PredictionResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PredictionResult.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea', 'model').order_by('-created_at')


class StartupFeatureVectorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StartupFeatureVectorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StartupFeatureVector.objects.filter(
            startup_idea__owner=self.request.user
        ).select_related('startup_idea')
