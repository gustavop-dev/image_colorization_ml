from django.urls import path
from colorizer.views.colorizer import colorize

app_name = 'colorizer'

urlpatterns = [
    path('colorize/', colorize, name='colorize'),
] 