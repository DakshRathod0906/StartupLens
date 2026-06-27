from rest_framework import serializers
from authentication.models import User, UserLoginHistory
from startup_ideas.models import StartupIdea, Tag, Industry
from research.models import ResearchJob, ResearchSource
from knowledge.models import Finding
from business_intelligence.models import Insight
from assessment.models import AssessmentRule, Assessment, OverallAssessment
from recommendations.models import RecommendationRule, Recommendation, RecommendationSummary
from roadmaps.models import TaskTemplate, Roadmap, RoadmapTask, RoadmapProgress
from evaluation.models import FinalEvaluation, EvaluationSnapshot
from reports.models import ReportTemplate, ReportSection, Report
from emails.models import NotificationPreference, NotificationTemplate, EmailLog
from investors.models import Investor, InvestmentPreference, StartupInvestorMatch, MatchExplanation
from ai.models import PromptTemplate, AIConversation, AIRequest
from ml.models import PredictionModel, PredictionResult, StartupFeatureVector


# ─── Authentication ───────────────────────────────────────────────

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'bio', 'role', 'is_verified', 'profile_picture',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']


class UserLoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginHistory
        fields = ['id', 'user', 'ip_address', 'user_agent', 'login_at', 'successful_login']
        read_only_fields = ['id', 'login_at']


# ─── Startup Ideas ────────────────────────────────────────────────

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name', 'slug', 'description', 'icon']


class StartupIdeaListSerializer(serializers.ModelSerializer):
    industry = IndustrySerializer(read_only=True)

    class Meta:
        model = StartupIdea
        fields = [
            'id', 'title', 'slug', 'short_description', 'industry',
            'status', 'startup_stage', 'version', 'created_at',
        ]


class StartupIdeaDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = StartupIdea
        fields = [
            'id', 'owner', 'title', 'slug', 'short_description',
            'problem_statement', 'proposed_solution', 'target_audience',
            'business_model', 'revenue_model', 'industry', 'tags',
            'status', 'startup_stage', 'version',
            'last_analyzed_at', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'owner', 'version', 'last_analyzed_at', 'created_at', 'updated_at']


class StartupIdeaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupIdea
        fields = [
            'title', 'short_description', 'problem_statement',
            'proposed_solution', 'target_audience', 'business_model',
            'revenue_model', 'industry', 'status', 'startup_stage',
        ]


# ─── Research ─────────────────────────────────────────────────────

class ResearchSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchSource
        fields = [
            'id', 'title', 'original_url', 'domain', 'provider',
            'status', 'excerpt', 'author', 'published_at',
            'credibility_score', 'created_at',
        ]


class ResearchJobSerializer(serializers.ModelSerializer):
    sources = ResearchSourceSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchJob
        fields = [
            'id', 'startup_idea', 'status', 'started_at', 'completed_at',
            'duration', 'total_sources', 'processed_sources',
            'failed_sources', 'duplicate_sources', 'created_at', 'sources',
        ]


# ─── Knowledge ────────────────────────────────────────────────────

class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = [
            'id', 'startup_idea', 'research_source', 'finding_type',
            'title', 'description', 'extractor_name', 'processing_status',
            'confidence_score', 'metadata', 'created_at',
        ]


# ─── Business Intelligence ────────────────────────────────────────

class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = [
            'id', 'startup_idea', 'generated_from_job', 'insight_type',
            'status', 'title', 'summary', 'confidence_score',
            'version', 'metadata', 'created_at',
        ]


# ─── Assessment ───────────────────────────────────────────────────

class AssessmentRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentRule
        fields = ['id', 'assessment_type', 'weight', 'minimum_score', 'maximum_score', 'is_active']


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            'id', 'startup_idea', 'assessment_type', 'score', 'max_score',
            'percentage', 'grade', 'summary', 'strengths', 'weaknesses',
            'status', 'version', 'metadata', 'created_at',
        ]


class OverallAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallAssessment
        fields = [
            'id', 'startup_idea', 'overall_score', 'grade',
            'version', 'summary', 'metadata', 'created_at',
        ]


# ─── Recommendations ─────────────────────────────────────────────

class RecommendationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationRule
        fields = [
            'id', 'metric', 'operator', 'minimum_value', 'maximum_value',
            'priority', 'rule_group', 'title', 'description',
            'recommended_action', 'is_active', 'display_order',
        ]


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = [
            'id', 'startup_idea', 'assessment', 'matched_rule',
            'priority', 'category', 'status', 'title', 'description',
            'recommended_action', 'version', 'is_resolved',
            'resolved_at', 'created_at',
        ]


class RecommendationSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationSummary
        fields = [
            'id', 'startup_idea', 'overall_priority', 'executive_summary',
            'total_recommendations', 'critical_count', 'high_count',
            'medium_count', 'low_count', 'optional_count',
            'version', 'overall_score_snapshot', 'overall_grade_snapshot',
            'created_at',
        ]


# ─── Roadmaps ─────────────────────────────────────────────────────

class RoadmapTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapTask
        fields = [
            'id', 'roadmap', 'recommendation', 'recommendation_title_snapshot',
            'recommendation_priority_snapshot', 'task_template',
            'phase', 'dependency_level', 'execution_order',
            'title', 'description', 'estimated_days',
            'scheduled_start_day', 'scheduled_end_day',
            'priority', 'status', 'started_at', 'completed_at',
        ]


class RoadmapProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapProgress
        fields = [
            'total_tasks', 'completed_tasks', 'blocked_tasks',
            'completion_percentage', 'remaining_days', 'last_updated',
        ]


class RoadmapSerializer(serializers.ModelSerializer):
    tasks = RoadmapTaskSerializer(many=True, read_only=True)
    progress = RoadmapProgressSerializer(read_only=True)

    class Meta:
        model = Roadmap
        fields = [
            'id', 'startup_idea', 'version', 'status', 'summary',
            'total_tasks', 'completed_tasks', 'blocked_tasks',
            'critical_tasks', 'completion_percentage',
            'overall_duration_days', 'estimated_completion',
            'created_at', 'tasks', 'progress',
        ]


# ─── Evaluation ───────────────────────────────────────────────────

class EvaluationSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationSnapshot
        fields = [
            'id', 'assessment_snapshot', 'recommendation_snapshot',
            'roadmap_snapshot', 'strength_snapshot', 'risk_snapshot',
            'summary_snapshot', 'overall_score_snapshot',
            'overall_grade_snapshot', 'created_at',
        ]


class FinalEvaluationSerializer(serializers.ModelSerializer):
    snapshot = EvaluationSnapshotSerializer(read_only=True)

    class Meta:
        model = FinalEvaluation
        fields = [
            'id', 'startup_idea', 'readiness_score', 'readiness_level',
            'overall_grade', 'executive_summary', 'key_strengths',
            'key_risks', 'critical_actions', 'confidence_score',
            'version', 'status', 'created_at', 'snapshot',
        ]


# ─── Reports ──────────────────────────────────────────────────────

class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ['id', 'name', 'description', 'version', 'is_active', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id', 'evaluation_snapshot', 'report_template',
            'generated_by', 'status', 'file_path', 'checksum',
            'version', 'created_at',
        ]
        read_only_fields = ['id', 'status', 'file_path', 'checksum', 'created_at']


# ─── Email ────────────────────────────────────────────────────────

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = '__all__'


class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = ['id', 'recipient_email', 'subject', 'status', 'sent_at']


# ─── Investors ────────────────────────────────────────────────────

class InvestmentPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPreference
        fields = [
            'id', 'industry', 'stage', 'country',
            'ticket_size_min', 'ticket_size_max', 'risk_appetite',
        ]


class InvestorSerializer(serializers.ModelSerializer):
    preferences = InvestmentPreferenceSerializer(read_only=True)

    class Meta:
        model = Investor
        fields = [
            'id', 'name', 'description', 'website',
            'contact_email', 'is_active', 'preferences', 'created_at',
        ]


class MatchExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchExplanation
        fields = ['matched_industries', 'matched_stage', 'matched_budget', 'reasoning']


class StartupInvestorMatchSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer(read_only=True)
    explanation = MatchExplanationSerializer(read_only=True)

    class Meta:
        model = StartupInvestorMatch
        fields = [
            'id', 'startup_idea', 'investor', 'compatibility_score',
            'match_status', 'matched_at', 'explanation',
        ]


# ─── AI ───────────────────────────────────────────────────────────

class PromptTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptTemplate
        fields = ['id', 'name', 'version', 'system_prompt', 'user_prompt', 'is_active', 'created_at']


class AIRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRequest
        fields = [
            'id', 'conversation', 'prompt_template', 'service_name',
            'model_name', 'input_hash', 'response', 'tokens_used',
            'latency_ms', 'status', 'created_at',
        ]


class AIConversationSerializer(serializers.ModelSerializer):
    requests = AIRequestSerializer(many=True, read_only=True)

    class Meta:
        model = AIConversation
        fields = ['id', 'startup_idea', 'title', 'created_at', 'updated_at', 'requests']


# ─── Machine Learning ────────────────────────────────────────────

class PredictionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionModel
        fields = [
            'id', 'name', 'algorithm', 'version', 'feature_schema_version',
            'accuracy', 'precision', 'recall', 'f1_score',
            'artifact_path', 'is_active', 'trained_at', 'created_at',
        ]


class StartupFeatureVectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupFeatureVector
        fields = ['id', 'startup_idea', 'schema_version', 'features', 'created_at']


class PredictionResultSerializer(serializers.ModelSerializer):
    model_info = PredictionModelSerializer(source='model', read_only=True)

    class Meta:
        model = PredictionResult
        fields = [
            'id', 'startup_idea', 'model', 'model_info',
            'predicted_success_probability', 'predicted_failure_probability',
            'feature_importances', 'created_at',
        ]
