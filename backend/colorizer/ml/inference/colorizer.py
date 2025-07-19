"""
Inference and colorization functionality for trained models.
"""

import numpy as np
import tensorflow as tf
import cv2
from pathlib import Path
from typing import Union

class ImageColorizer:
    """
    Handles inference and colorization of grayscale images.
    """
    
    def __init__(self, model: tf.keras.Model, img_size: int = 256):
        """
        Initialize the colorizer with a trained model.
        
        Args:
            model (tf.keras.Model): The trained colorization model
            img_size (int): Size of input images
        """
        self.model = model
        self.img_size = img_size
    
    def colorize(self, image_path: Union[str, Path], save_to: Union[str, Path, None] = None) -> np.ndarray:
        """
        Colorize a single grayscale image using the trained model.
        
        This method loads a grayscale image, preprocesses it, runs inference
        through the model, and returns the colorized result.
        
        Args:
            image_path (Union[str, Path]): Path to input grayscale image
            save_to (Union[str, Path, None]): Optional path to save colorized output
            
        Returns:
            np.ndarray: Colorized image array in uint8 RGB format
            
        Raises:
            RuntimeError: If the model hasn't been provided
        """
        if self.model is None:
            raise RuntimeError("Model not built. Call build_model() first.")

        # Load and preprocess the input image
        img = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(img_rgb, (self.img_size, self.img_size))
        
        # Normalize and add batch dimension
        inp = (img_rgb.astype(np.float32) / 255.0)[None, ...]  # shape (1, H, W, 3)

        # Run inference through the model
        pred = self.model.predict(inp)[0]  # Remove batch dimension: (H, W, 3)
        
        # Convert back to uint8 format and clip values to valid range
        pred = np.clip(pred * 255.0, 0, 255).astype(np.uint8)

        # Save output if requested
        if save_to is not None:
            Path(save_to).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(save_to), cv2.cvtColor(pred, cv2.COLOR_RGB2BGR))

        return pred
    
    def save_model(self, path: Union[str, Path]) -> None:
        """
        Save the trained model to disk.
        
        This method saves the entire model (architecture + weights) to the
        specified path in TensorFlow's SavedModel format.
        
        Args:
            path (Union[str, Path]): Path where the model should be saved
            
        Raises:
            RuntimeError: If the model hasn't been provided
        """
        if self.model is None:
            raise RuntimeError("Model not built. Call build_model() first.")
        
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.model.save(str(path))
        print(f"Model saved to {path}") 