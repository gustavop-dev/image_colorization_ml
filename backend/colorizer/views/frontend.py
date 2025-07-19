"""
Vista para servir el frontend de Vue.js compilado.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def index(request: HttpRequest) -> HttpResponse:
    """
    Sirve la página principal del frontend de Vue.js.
    
    Esta vista renderiza el template index.html que contiene
    la aplicación Vue.js compilada con todos sus assets.
    
    Args:
        request (HttpRequest): El objeto de solicitud HTTP
        
    Returns:
        HttpResponse: La respuesta con el template renderizado
    """
    return render(request, 'index.html') 