"""
Image Colorization Model Module

This module provides backward compatibility by importing the refactored 
ColorizationModel from the new modular structure in the ml/ subdirectory.

The model has been refactored into separate modules for better organization:
- ml/models/: Contains U-Net architecture and main model class
- ml/data/: Contains dataset loading and image utilities
- ml/training/: Contains training and evaluation logic
- ml/inference/: Contains colorization and model persistence

Author: Image Colorization ML Team
Date: 2024
"""

# Import the refactored ColorizationModel from the ml subdirectory
from .ml import ColorizationModel

# Export for backward compatibility
__all__ = ['ColorizationModel'] 