from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ImageColorization
from .serializers import ImageColorizationSerializer, ImageUploadSerializer
from .ml_model import ColorizationModel
import os
from django.conf import settings
import threading

# Initialize the colorization model
colorization_model = ColorizationModel()

def process_image_async(image_id):
    """Process image colorization in a separate thread"""
    # Get the image object
    image_obj = ImageColorization.objects.get(id=image_id)
    
    # Get the file paths
    original_path = image_obj.original_image.path
    
    # Create output path
    filename = os.path.basename(original_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(settings.MEDIA_ROOT, 'images', 'colorized', f"{name}_colorized{ext}")
    
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Colorize the image
    colorization_model.colorize(original_path, output_path)
    
    # Update the model with the colorized image path
    relative_path = os.path.join('images', 'colorized', f"{name}_colorized{ext}")
    image_obj.colorized_image = relative_path
    image_obj.processed = True
    image_obj.save()

@api_view(['POST'])
def upload_image(request):
    """Upload an image for colorization"""
    serializer = ImageUploadSerializer(data=request.data)
    
    if serializer.is_valid():
        # Create a new ImageColorization object
        image_obj = ImageColorization(
            original_image=serializer.validated_data['image']
        )
        image_obj.save()
        
        # Start the colorization process in a separate thread
        threading.Thread(
            target=process_image_async,
            args=(image_obj.id,)
        ).start()
        
        # Return the image object data
        return Response(
            ImageColorizationSerializer(image_obj).data,
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def colorize_image(request):
    """Get the status of a colorization process"""
    image_id = request.query_params.get('id')
    
    if not image_id:
        return Response(
            {"error": "Image ID is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    image_obj = get_object_or_404(ImageColorization, id=image_id)
    return Response(ImageColorizationSerializer(image_obj).data)

@api_view(['GET'])
def image_history(request):
    """Get a list of all processed images"""
    images = ImageColorization.objects.all()
    serializer = ImageColorizationSerializer(images, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_image(request, image_id):
    """Get details for a specific image"""
    image_obj = get_object_or_404(ImageColorization, id=image_id)
    return Response(ImageColorizationSerializer(image_obj).data)
