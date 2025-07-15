"""
Machine Learning package for image colorization.

This package contains all the machine learning components for the image colorization system:
- Model architectures (U-Net)
- Data loading and preprocessing
- Training and evaluation
- Inference and colorization

The main entry point is the ColorizationModel class.
"""

from .core import ColorizationModel

__all__ = ['ColorizationModel'] 