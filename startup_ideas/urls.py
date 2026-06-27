from django.urls import path
from . import views

app_name = 'startup_ideas'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.idea_list_view, name='list'),
    path('create/', views.idea_create_view, name='create'),
    path('<slug:slug>/', views.idea_detail_view, name='detail'),
    path('<slug:slug>/edit/', views.idea_edit_view, name='edit'),
    path('<slug:slug>/archive/', views.idea_archive_view, name='archive'),
    path('<slug:slug>/restore/', views.idea_restore_view, name='restore'),
    path('<slug:slug>/delete/', views.idea_delete_view, name='delete'),
    
    # Analysis Endpoints
    path('<slug:slug>/analyze/', views.run_analysis_view, name='run_analysis'),
    path('<slug:slug>/post-process/<str:action>/', views.post_processing_view, name='post_process'),
    path('<slug:slug>/analysis-status/', views.analysis_status_api, name='analysis_status'),
]
