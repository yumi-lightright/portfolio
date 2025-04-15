from django.shortcuts import render
from django.views.generic import TemplateView


class TopView(TemplateView):
    template_name = "data_analysis/top.html"  # 使用するテンプレートを指定

def home(request):
    return render(request, 'data_analysis/base.html')  # header、nav、footer

def about(request):
    return render(request, 'data_analysis/about.html')  # Aboutページのテンプレート指定

def skillanalyzar(request):
    return render(request, 'data_analysis/skillanalyzar.html')  # skillanalyzarページのテンプレート指定