# views.py

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def api_view(request):
    return render(request, 'api.html')

def result_view(request):
    return render(request, 'result.html')
