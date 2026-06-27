"""
URL configuration for StartupLens project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('auth/', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('ideas/', include('startup_ideas.urls')),
    path('research/', include('research.urls')),
    path('knowledge/', include('knowledge.urls')),
    path('bi/', include('business_intelligence.urls')),
    path('assessment/', include('assessment.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('roadmaps/', include('roadmaps.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
