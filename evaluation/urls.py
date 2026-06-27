from django.urls import path
from . import views

app_name = 'evaluation'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('<int:pk>/', views.EvaluationDetailView.as_view(), name='evaluation_detail'),
    path('<int:pk>/history/', views.EvaluationHistoryView.as_view(), name='evaluation_history'),
    path('<int:pk>/executive-summary/', views.ExecutiveSummaryView.as_view(), name='executive_summary'),
    path('<int:pk>/decision-breakdown/', views.DecisionBreakdownView.as_view(), name='decision_breakdown'),
]
