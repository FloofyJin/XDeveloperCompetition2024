# urls.py in InterestsApp

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', views.api_view, name='api'),
]
