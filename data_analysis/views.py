from django.shortcuts import render
from django.views.generic import TemplateView

class TopView(TemplateView):
    template_name = "data_analysis/top.html"  # 使用するテンプレートを指定

