from django.urls import path
from . import views

app_name = 'knowledge'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('findings/', views.finding_list_view, name='finding_list'),
    path('findings/<int:finding_id>/', views.finding_detail_view, name='finding_detail'),
]
