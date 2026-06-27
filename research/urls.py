from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('jobs/', views.job_list_view, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('sources/', views.source_list_view, name='source_list'),
    path('sources/<int:source_id>/', views.source_detail_view, name='source_detail'),
]
