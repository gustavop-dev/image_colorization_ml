import logging
from pathlib import Path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse

from ..ml.services import colorization_service
from ..utils import (
    validate_image_file,
    save_uploaded_file,
    create_temp_output_path,
    cleanup_temp_files,
    create_image_response
)

logger = logging.getLogger(__name__)

@api_view(['POST'])
def colorize(request):
    """
    Colorize a grayscale image using the trained deep learning model.
    
    Expects:
        - POST request with 'image' file in form-data
        - Image should be in grayscale/black and white
        - Supported formats: JPG, JPEG, PNG, BMP
        - Max file size: 10MB
    
    Returns:
        - Success: Colorized image file
        - Error: JSON response with error details
    """
    # Check if image was sent in request
    if 'image' not in request.FILES:
        return Response(
            {"error": "No image file provided. Please send an image in the 'image' field."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    uploaded_file = request.FILES['image']
    
    # Validate the uploaded image
    is_valid, error_message = validate_image_file(uploaded_file)
    if not is_valid:
        return Response(
            {"error": f"Invalid image file: {error_message}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    # Check if model is loaded
    if not colorization_service.is_model_loaded():
        logger.error("Colorization model is not loaded")
        return Response(
            {"error": "Colorization service is not available. Please try again later."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    
    input_path = None
    output_path = None
    
    try:
        # Save uploaded file to temporary location
        input_path = save_uploaded_file(uploaded_file, prefix="grayscale")
        logger.info(f"Processing image: {input_path.name}")
        
        # Create output path
        output_path = create_temp_output_path(input_path)
        
        # Perform colorization using the trained model
        logger.info("Starting colorization process...")
        colorized_image = colorization_service.colorize_image(input_path, output_path)
        logger.info("Colorization completed successfully")
        
        # Create response with colorized image
        colorized_filename = f"colorized_{uploaded_file.name}"
        response = create_image_response(output_path, filename=colorized_filename)
        
        # Schedule cleanup of temporary files after response is sent
        # Note: Files will be cleaned up after the response is fully sent
        def cleanup_after_response():
            cleanup_temp_files(input_path, output_path)
        
        # Add cleanup callback (this will run after response is sent)
        response.close_callback = cleanup_after_response
        
        return response

    except Exception as e:
        logger.error(f"Error during colorization: {str(e)}", exc_info=True)
        
        # Cleanup temporary files in case of error
        if input_path or output_path:
            cleanup_temp_files(input_path, output_path)
        
        return Response(
            {"error": "An error occurred during image colorization. Please try again."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(['GET'])
def health_check(request):
    """
    Check if the colorization service is ready to process images.
    
    Returns:
        JSON response with service status
    """
    try:
        is_loaded = colorization_service.is_model_loaded()
        
        return Response({
            "status": "healthy" if is_loaded else "unhealthy",
            "model_loaded": is_loaded,
            "service": "Image Colorization API"
        }, status=status.HTTP_200_OK if is_loaded else status.HTTP_503_SERVICE_UNAVAILABLE)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return Response({
            "status": "unhealthy",
            "model_loaded": False,
            "error": "Service unavailable"
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE) 