"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# We can use this file to add links to html files

from django.contrib import admin
from django.urls import path, include
from . import views
from .views import home, fetch_youtube_videos, main_view, threat_data

urlpatterns = [
    path('', views.login_view, name='login'),
    path('api/threats/', threat_data, name='threat_data'),
    path('home/', views.home, name='home'),
    path('fetch_youtube_videos/', views.fetch_youtube_videos, name='fetch_youtube_videos'),
    path('start_scan/', views.start_scan, name='start_scan'),
    path('send_email/', views.send_email, name='send_email'),
    path('generate_email_content/', views.generate_email_content, name='generate_email_content'),
    path('main/', main_view, name='main_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),

]

