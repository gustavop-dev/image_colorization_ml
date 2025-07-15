"""
Training and evaluation functionality for image colorization models.
"""

import tensorflow as tf
from typing import List

class ModelTrainer:
    """
    Handles training and evaluation of colorization models.
    """
    
    def __init__(self, model: tf.keras.Model):
        """
        Initialize the trainer with a model.
        
        Args:
            model (tf.keras.Model): The compiled model to train
        """
        self.model = model
    
    def train(self, train_gray, train_color, val_gray, val_color, epochs: int = 50, batch_size: int = 32) -> tf.keras.callbacks.History:
        """
        Train the colorization model on the loaded dataset.
        
        This method trains the U-Net model using the loaded training data,
        with validation performed on the validation set at each epoch.
        
        Args:
            train_gray: Training grayscale images
            train_color: Training color images
            val_gray: Validation grayscale images
            val_color: Validation color images
            epochs (int): Number of training epochs (default: 50)
            batch_size (int): Batch size for training (default: 32)
            
        Returns:
            tf.keras.callbacks.History: Training history containing loss and metrics
            
        Raises:
            RuntimeError: If model hasn't been provided
        """
        if self.model is None:
            raise RuntimeError("Model not built. Call build_model() first.")

        # Train the model with validation
        history = self.model.fit(
            train_gray,    # Input: grayscale images
            train_color,   # Target: color images
            validation_data=(val_gray, val_color),
            epochs=epochs,
            batch_size=batch_size,
            verbose=True,       # Show training progress
        )
        return history      
    
    def evaluate(self, val_gray, val_color) -> List[float]:
        """
        Evaluate the trained model on validation data.
        
        This method computes the loss and accuracy metrics on the validation set
        to assess model performance.
        
        Args:
            val_gray: Validation grayscale images
            val_color: Validation color images
        
        Returns:
            List[float]: List containing validation loss and metrics
            
        Raises:
            RuntimeError: If model hasn't been provided
        """
        if self.model is None:
            raise RuntimeError("Model not built. Call build_model() first.")
            
        return self.model.evaluate(val_gray, val_color) 