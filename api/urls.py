from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()

# Authentication
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'login-history', views.UserLoginHistoryViewSet, basename='login-history')

# Startup Ideas
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'industries', views.IndustryViewSet, basename='industry')
router.register(r'startup-ideas', views.StartupIdeaViewSet, basename='startup-idea')

# Research
router.register(r'research-jobs', views.ResearchJobViewSet, basename='research-job')
router.register(r'research-sources', views.ResearchSourceViewSet, basename='research-source')

# Knowledge
router.register(r'findings', views.FindingViewSet, basename='finding')

# Business Intelligence
router.register(r'insights', views.InsightViewSet, basename='insight')

# Assessment
router.register(r'assessment-rules', views.AssessmentRuleViewSet, basename='assessment-rule')
router.register(r'assessments', views.AssessmentViewSet, basename='assessment')
router.register(r'overall-assessments', views.OverallAssessmentViewSet, basename='overall-assessment')

# Recommendations
router.register(r'recommendation-rules', views.RecommendationRuleViewSet, basename='recommendation-rule')
router.register(r'recommendations', views.RecommendationViewSet, basename='recommendation')
router.register(r'recommendation-summaries', views.RecommendationSummaryViewSet, basename='recommendation-summary')

# Roadmaps
router.register(r'roadmaps', views.RoadmapViewSet, basename='roadmap')
router.register(r'roadmap-tasks', views.RoadmapTaskViewSet, basename='roadmap-task')

# Evaluation
router.register(r'evaluations', views.FinalEvaluationViewSet, basename='evaluation')

# Reports
router.register(r'report-templates', views.ReportTemplateViewSet, basename='report-template')
router.register(r'reports', views.ReportViewSet, basename='report')

# Email
router.register(r'notification-preferences', views.NotificationPreferenceViewSet, basename='notification-preference')
router.register(r'email-logs', views.EmailLogViewSet, basename='email-log')

# Investors
router.register(r'investors', views.InvestorViewSet, basename='investor')
router.register(r'investor-matches', views.StartupInvestorMatchViewSet, basename='investor-match')

# AI
router.register(r'prompt-templates', views.PromptTemplateViewSet, basename='prompt-template')
router.register(r'ai-conversations', views.AIConversationViewSet, basename='ai-conversation')
router.register(r'ai-requests', views.AIRequestViewSet, basename='ai-request')

# Machine Learning
router.register(r'prediction-models', views.PredictionModelViewSet, basename='prediction-model')
router.register(r'predictions', views.PredictionResultViewSet, basename='prediction')
router.register(r'feature-vectors', views.StartupFeatureVectorViewSet, basename='feature-vector')

urlpatterns = [
    path('', include(router.urls)),
]
