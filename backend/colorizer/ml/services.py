"""
Service layer for managing the colorization model in production.

This module provides a singleton-style model manager to ensure the heavy
model is loaded only once and reused across multiple requests.
"""

import logging
from typing import Optional
from pathlib import Path

from .models.colorization_model import ColorizationModel
from .config import COLORIZATION_MODEL_PATH, MODEL_INPUT_SIZE, AUTO_COMPRESS, MAX_FILE_SIZE_MB

logger = logging.getLogger(__name__)

class ColorizationService:
    """
    Singleton-style service for managing the colorization model.
    
    This service ensures that the trained model is loaded only once
    and can be reused across multiple HTTP requests efficiently.
    """
    
    _instance: Optional['ColorizationService'] = None
    _model: Optional[ColorizationModel] = None
    _is_loaded: bool = False
    
    def __new__(cls) -> 'ColorizationService':
        """Ensure only one instance of the service exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the service (called only once)."""
        if not hasattr(self, 'initialized'):
            self.initialized = True
            logger.info("Initializing ColorizationService")
    
    def load_model(self, model_path: Optional[Path] = None) -> None:
        """
        Load the trained colorization model.
        
        Args:
            model_path (Optional[Path]): Path to model file. 
                                       Uses default if None.
        
        Raises:
            FileNotFoundError: If model file doesn't exist
            ValueError: If model loading fails
        """
        if self._is_loaded and self._model is not None:
            logger.info("Model already loaded, skipping reload")
            return
        
        model_path = model_path or COLORIZATION_MODEL_PATH
        
        try:
            logger.info(f"Loading colorization model from {model_path}")
            self._model = ColorizationModel(img_size=MODEL_INPUT_SIZE)
            self._model.load_trained_model(model_path)
            self._is_loaded = True
            logger.info("Colorization model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load colorization model: {e}")
            self._model = None
            self._is_loaded = False
            raise
    
    def get_model(self) -> ColorizationModel:
        """
        Get the loaded colorization model.
        
        Returns:
            ColorizationModel: The loaded model instance
            
        Raises:
            RuntimeError: If model hasn't been loaded yet
        """
        if not self._is_loaded or self._model is None:
            raise RuntimeError(
                "Model not loaded. Call load_model() first or check if model file exists."
            )
        
        return self._model
    
    def is_model_loaded(self) -> bool:
        """
        Check if the model is currently loaded.
        
        Returns:
            bool: True if model is loaded and ready for use
        """
        return self._is_loaded and self._model is not None
    
    def colorize_image(self, input_path: Path, output_path: Optional[Path] = None, use_patches: bool = True, auto_compress: Optional[bool] = None, max_size_mb: Optional[float] = None):
        """
        Colorize an image using the loaded model with smart compression.
        
        Args:
            input_path (Path): Path to input grayscale image
            output_path (Optional[Path]): Path to save colorized image
            use_patches (bool): Whether to use patch-based processing
            auto_compress (Optional[bool]): Whether to auto-compress large images 
                                          (uses config default if None)
            max_size_mb (Optional[float]): Max file size before compression
                                         (uses config default if None)
            
        Returns:
            np.ndarray: Colorized image array
            
        Raises:
            RuntimeError: If model isn't loaded
        """
        model = self.get_model()
        
        # Use config defaults if not specified
        if auto_compress is None:
            auto_compress = AUTO_COMPRESS
        if max_size_mb is None:
            max_size_mb = MAX_FILE_SIZE_MB
            
        return model.colorize(
            input_path, 
            output_path, 
            use_patches=use_patches,
            auto_compress=auto_compress,
            max_size_mb=max_size_mb
        )

# Global service instance
colorization_service = ColorizationService() 