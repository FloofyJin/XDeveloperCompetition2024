from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('choices/<str:search_query>/', views.choices, name='choices'),
]
