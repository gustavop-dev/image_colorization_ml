"""
Configuration settings for the ML colorization module.
"""

import os
from pathlib import Path

# Base directory of the ML module
ML_BASE_DIR = Path(__file__).parent

# Directory containing trained models
TRAINED_MODELS_DIR = ML_BASE_DIR / "trained_models"

# Path to the main colorization model
COLORIZATION_MODEL_PATH = TRAINED_MODELS_DIR / "colorization_model.h5"

# Model settings
MODEL_INPUT_SIZE = 256  # Image size the model expects

# High-resolution processing settings
USE_PATCH_PROCESSING = True  # Enable patch processing for high-res images
PATCH_SIZE = 256            # Size of each patch (should match MODEL_INPUT_SIZE)
PATCH_OVERLAP = 32          # Overlap between patches for smooth blending
MIN_SIZE_FOR_PATCHES = 256  # Minimum image size to trigger patch processing

# Auto-compression settings (WhatsApp-style)
AUTO_COMPRESS = True        # Enable automatic compression for large images
MAX_FILE_SIZE_MB = 1.0      # Maximum file size before compression (1MB)
MAX_DIMENSION_COMPRESSED = 1600  # Maximum dimension after compression (WhatsApp uses ~1600px)
COMPRESSION_QUALITY_LEVELS = [85, 75, 65, 55, 45, 35, 25]  # Progressive quality reduction

# File upload settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max file size
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']  # Include WEBP support

# Temporary file settings
TEMP_DIR = Path("/tmp/colorization")
TEMP_DIR.mkdir(exist_ok=True) 