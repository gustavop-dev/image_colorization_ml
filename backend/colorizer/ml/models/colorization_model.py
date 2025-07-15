"""
Main colorization model that orchestrates all components.
"""

import numpy as np
import tensorflow as tf
import pathlib as Path
from typing import List

from ..data.dataset_loader import DatasetLoader
from ..training.trainer import ModelTrainer
from ..inference.colorizer import ImageColorizer
from .unet import UNetModel

class ColorizationModel:
    """
    A deep learning model for image colorization using U-Net architecture.
    
    This class provides functionality to:
    - Load and preprocess image datasets
    - Build and train a U-Net model for colorization
    - Perform inference on grayscale images
    - Save and evaluate trained models
    
    Attributes:
        model (tf.keras.Model): The U-Net model for colorization
        img_size (int): Size of input images (default: 256x256)
        input_shape (tuple): Shape of input tensors (height, width, channels)
        initialized (bool): Whether the model has been built
        dataset_loader (DatasetLoader): Handles dataset loading
        trainer (ModelTrainer): Handles training and evaluation
        colorizer (ImageColorizer): Handles inference and colorization
    """
    
    def __init__(self, img_size: int = 256):
        """
        Initialize the colorization model.
        
        Args:
            img_size (int): Size of input images. Images will be resized to 
                          (img_size, img_size) for training and inference.
        """
        self.model = None
        self.img_size = img_size  
        self.input_shape = (img_size, img_size, 3)  # RGB format
        self.initialized = False
        
        # Initialize components
        self.dataset_loader = DatasetLoader(img_size)
        self.unet_builder = UNetModel(img_size)
        self.trainer = None
        self.colorizer = None
        
        # Store dataset references
        self.train_gray = None
        self.train_color = None
        self.val_gray = None
        self.val_color = None
    
    def load_dataset(self, color_dir: str | Path, gray_dir: str | Path, train_split: float = 0.8) -> None:
        """
        Load and prepare the training dataset.
        
        This method loads paired color and grayscale images from the specified directories,
        performs preprocessing, and splits the data into training and validation sets.
        
        Args:
            color_dir (str | Path): Directory containing color (target) images
            gray_dir (str | Path): Directory containing grayscale (input) images
            train_split (float): Fraction of data to use for training (default: 0.8)
            
        Raises:
            ValueError: If the number of color and grayscale images don't match
        """
        self.train_gray, self.train_color, self.val_gray, self.val_color = self.dataset_loader.load_dataset(
            color_dir, gray_dir, train_split
        )
    
    def build_model(self) -> tf.keras.Model:
        """
        Build and compile the U-Net model for image colorization.
        
        The U-Net architecture consists of:
        - Encoder: Downsampling path that captures context
        - Decoder: Upsampling path that enables precise localization
        - Skip connections: Direct connections between encoder and decoder layers
        
        Returns:
            tf.keras.Model: Compiled U-Net model ready for training
        """
        self.model = self.unet_builder.build_model()
        self.trainer = ModelTrainer(self.model)
        self.colorizer = ImageColorizer(self.model, self.img_size)
        return self.model
    
    def train(self, epochs: int = 50, batch_size: int = 32) -> tf.keras.callbacks.History:
        """
        Train the colorization model on the loaded dataset.
        
        This method trains the U-Net model using the loaded training data,
        with validation performed on the validation set at each epoch.
        
        Args:
            epochs (int): Number of training epochs (default: 50)
            batch_size (int): Batch size for training (default: 32)
            
        Returns:
            tf.keras.callbacks.History: Training history containing loss and metrics
            
        Raises:
            RuntimeError: If model hasn't been built or dataset hasn't been loaded
        """
        if self.trainer is None:
            raise RuntimeError("Model not built. Call build_model() first.")
        if self.train_gray is None:
            raise RuntimeError("Dataset not loaded. Call load_dataset() first.")
        
        return self.trainer.train(
            self.train_gray, self.train_color, 
            self.val_gray, self.val_color, 
            epochs, batch_size
        )
    
    def evaluate(self) -> List[float]:
        """
        Evaluate the trained model on validation data.
        
        This method computes the loss and accuracy metrics on the validation set
        to assess model performance.
        
        Returns:
            List[float]: List containing validation loss and metrics
            
        Raises:
            RuntimeError: If model hasn't been built or dataset hasn't been loaded
        """
        if self.trainer is None:
            raise RuntimeError("Model not built. Call build_model() first.")
        if self.val_gray is None:
            raise RuntimeError("Dataset not loaded. Call load_dataset() first.")
        
        return self.trainer.evaluate(self.val_gray, self.val_color)
    
    def colorize(self, image_path: str | Path, save_to: str | Path | None = None) -> np.ndarray:
        """
        Colorize a single grayscale image using the trained model.
        
        This method loads a grayscale image, preprocesses it, runs inference
        through the model, and returns the colorized result.
        
        Args:
            image_path (str | Path): Path to input grayscale image
            save_to (str | Path | None): Optional path to save colorized output
            
        Returns:
            np.ndarray: Colorized image array in uint8 RGB format
            
        Raises:
            RuntimeError: If the model hasn't been built yet
        """
        if self.colorizer is None:
            raise RuntimeError("Model not built. Call build_model() first.")
        
        return self.colorizer.colorize(image_path, save_to)
    
    def save_model(self, path: str | Path) -> None:
        """
        Save the trained model to disk.
        
        This method saves the entire model (architecture + weights) to the
        specified path in TensorFlow's SavedModel format.
        
        Args:
            path (str | Path): Path where the model should be saved
            
        Raises:
            RuntimeError: If the model hasn't been built yet
        """
        if self.colorizer is None:
            raise RuntimeError("Model not built. Call build_model() first.")
        
        self.colorizer.save_model(path) 