from django.urls import path
from . import views

app_name = 'colorizer'

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('colorize/', views.colorize_image, name='colorize_image'),
    path('history/', views.image_history, name='image_history'),
    path('image/<int:image_id>/', views.get_image, name='get_image'),
] 