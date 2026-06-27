from django.urls import path
from . import views

app_name = 'business_intelligence'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('insights/', views.insight_list_view, name='insight_list'),
    path('insights/<int:insight_id>/', views.insight_detail_view, name='insight_detail'),
]
