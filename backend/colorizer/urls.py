from django.urls import path
from colorizer.views.colorizer import colorize, health_check

app_name = 'colorizer'

urlpatterns = [
    path('colorize/', colorize, name='colorize'),
    path('health/', health_check, name='health_check'),
] 