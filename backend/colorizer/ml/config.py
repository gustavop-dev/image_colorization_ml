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

# File upload settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max file size
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']

# Temporary file settings
TEMP_DIR = Path("/tmp/colorization")
TEMP_DIR.mkdir(exist_ok=True) 