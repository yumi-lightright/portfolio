from django.shortcuts import render
from django.views.generic import TemplateView


class TopView(TemplateView):
    template_name = "data_analysis/top.html"  # 使用するテンプレートを指定

from django.shortcuts import render
def home(request):
    return render(request, 'data_analysis/base.html')  # header、nav、footer