from django.urls import path
from . import views

app_name = 'roadmaps'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('<int:roadmap_id>/', views.roadmap_detail_view, name='roadmap_detail'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('history/<int:idea_id>/', views.roadmap_history_view, name='roadmap_history'),
]
