from django.urls import path
from colorizer.views.colorizer import colorize, health_check
from colorizer.views.frontend import index

app_name = 'colorizer'

urlpatterns = [
    # API endpoints
    path('api/colorize/', colorize, name='colorize'),
    path('api/health/', health_check, name='health_check'),
    
    # Frontend routes
    path('', index, name='frontend'),  # Página principal (Vue.js app)
] 