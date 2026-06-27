from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('list/', views.recommendation_list_view, name='recommendation_list'),
    path('<int:recommendation_id>/', views.recommendation_detail_view, name='recommendation_detail'),
    path('<int:recommendation_id>/history/', views.recommendation_history_view, name='recommendation_history'),
    path('summary/<int:summary_id>/', views.summary_view, name='summary_detail'),
]
