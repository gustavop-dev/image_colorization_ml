"""
Core Image Colorization Model Module

This is the main module of the ML package that provides the ColorizationModel class.
It imports and orchestrates components from the specialized modules:

- models/: Contains U-Net architecture and main model class
- data/: Contains dataset loading and image utilities
- training/: Contains training and evaluation logic
- inference/: Contains colorization and model persistence

Author: Image Colorization ML Team
Date: 2024
"""

# Import the refactored ColorizationModel
from .models.colorization_model import ColorizationModel

# Export for backward compatibility
__all__ = ['ColorizationModel'] 