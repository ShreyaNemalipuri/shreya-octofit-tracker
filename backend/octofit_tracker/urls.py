"""
URL configuration for octofit_tracker project.
"""

import os
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Get codespace name for URL construction
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('profiles.urls')),
    path('api/', include('activities.urls')),
    path('api/', include('teams.urls')),
    path('api/', include('leaderboards.urls')),
]
