from django.urls import path
from . import views

app_name = 'assessment'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('assessments/', views.assessment_list_view, name='assessment_list'),
    path('assessments/<int:assessment_id>/', views.assessment_detail_view, name='assessment_detail'),
    path('assessments/<int:assessment_id>/history/', views.assessment_history_view, name='assessment_history'),
]
