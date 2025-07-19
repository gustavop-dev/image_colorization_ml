"""
Utility functions for handling image files in Django views.
"""

import os
import uuid
import logging
from pathlib import Path
from typing import Tuple, Optional
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, FileResponse
from PIL import Image  # For comprehensive image validation and processing

from .ml.config import (
    MAX_FILE_SIZE, 
    ALLOWED_IMAGE_EXTENSIONS, 
    TEMP_DIR
)

logger = logging.getLogger(__name__)

def validate_image_file(uploaded_file: UploadedFile) -> Tuple[bool, str]:
    """
    Validate an uploaded image file.
    
    Args:
        uploaded_file (UploadedFile): The uploaded file from Django request
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Check file size
    if uploaded_file.size > MAX_FILE_SIZE:
        return False, f"File size too large. Maximum allowed: {MAX_FILE_SIZE // (1024*1024)}MB"
    
    # Check file extension
    file_extension = Path(uploaded_file.name).suffix.lower()
    if file_extension not in ALLOWED_IMAGE_EXTENSIONS:
        return False, f"Invalid file type. Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
    
    # Try to open as image using PIL for comprehensive validation
    try:
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        image.verify()  # Verify it's a valid image
        uploaded_file.seek(0)  # Reset again for later use
        
        # Additional checks
        if image.size[0] < 10 or image.size[1] < 10:
            return False, "Image too small (minimum 10x10 pixels)"
        
        if image.size[0] > 10000 or image.size[1] > 10000:
            return False, "Image too large (maximum 10000x10000 pixels)"
        
        # Verify supported format (PIL can open more than we want to support)
        if image.format not in ['JPEG', 'PNG', 'WEBP']:
            return False, f"Unsupported image format: {image.format}. Supported: JPEG, PNG, WEBP"
        
        return True, ""
        
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"

def save_uploaded_file(uploaded_file: UploadedFile, prefix: str = "input") -> Path:
    """
    Save an uploaded file to a temporary location.
    
    Args:
        uploaded_file (UploadedFile): The uploaded file
        prefix (str): Prefix for the temporary filename
        
    Returns:
        Path: Path to the saved temporary file
    """
    # Generate unique filename
    file_extension = Path(uploaded_file.name).suffix.lower()
    unique_filename = f"{prefix}_{uuid.uuid4().hex}{file_extension}"
    temp_path = TEMP_DIR / unique_filename
    
    # Save file
    with open(temp_path, 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)
    
    logger.info(f"Saved uploaded file to {temp_path}")
    return temp_path

def create_temp_output_path(input_path: Path) -> Path:
    """
    Create a temporary output path based on input path.
    
    Args:
        input_path (Path): Path to input file
        
    Returns:
        Path: Path for output file
    """
    input_stem = input_path.stem
    file_extension = input_path.suffix
    output_filename = f"colorized_{input_stem}_{uuid.uuid4().hex[:8]}{file_extension}"
    return TEMP_DIR / output_filename

def cleanup_temp_files(*file_paths: Path) -> None:
    """
    Clean up temporary files.
    
    Args:
        *file_paths: Variable number of file paths to delete
    """
    for file_path in file_paths:
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {e}")

def create_image_response(image_path: Path, filename: Optional[str] = None) -> FileResponse:
    """
    Create a Django FileResponse for an image file.
    
    Args:
        image_path (Path): Path to the image file
        filename (Optional[str]): Optional custom filename for download
        
    Returns:
        FileResponse: Django response with the image file
    """
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Determine content type based on file extension
    extension = image_path.suffix.lower()
    content_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.webp': 'image/webp',
    }
    content_type = content_type_map.get(extension, 'image/jpeg')
    
    # Create response
    response = FileResponse(
        open(image_path, 'rb'),
        content_type=content_type
    )
    
    # Set filename for download
    if filename:
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response 