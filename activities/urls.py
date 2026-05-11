from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_choice, name='submit_choice'),
    path('success/', views.success, name='success'),
]
