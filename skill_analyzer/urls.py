"""
URL configuration for skill_analyzer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from data_analysis import views
from data_analysis.views import TopView, home, about, skillanalyzer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TopView.as_view(), name="top"),       # トップページ
    path('base/', home, name="base_template"),            # ベーステンプレートビュー
    path('about/', views.about, name="about"),        # Aboutページ
    path('skillanalyzer/', views.skillanalyzer, name="skillanalyzer"),  # スキル分析ページ
    path('explanation/', views.explanation, name="explanation"),  # 説明ページ
]
