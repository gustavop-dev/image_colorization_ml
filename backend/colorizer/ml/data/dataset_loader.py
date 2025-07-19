"""
Dataset loading and preprocessing for image colorization.
"""

import numpy as np
from pathlib import Path
from typing import Tuple, Union
from .image_utils import ImageUtils

class DatasetLoader:
    """
    Handles loading and preprocessing of image datasets for colorization.
    """
    
    def __init__(self, img_size: int = 256):
        """
        Initialize the dataset loader.
        
        Args:
            img_size (int): Size of input images. Images will be resized to 
                          (img_size, img_size) for training and inference.
        """
        self.img_size = img_size
        self.train_gray = None
        self.train_color = None
        self.val_gray = None
        self.val_color = None
    
    def load_dataset(self, color_dir: Union[str, Path], gray_dir: Union[str, Path], train_split: float = 0.8) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Load and prepare the training dataset.
        
        This method loads paired color and grayscale images from the specified directories,
        performs preprocessing, and splits the data into training and validation sets.
        
        Args:
            color_dir (Union[str, Path]): Directory containing color (target) images
            gray_dir (Union[str, Path]): Directory containing grayscale (input) images
            train_split (float): Fraction of data to use for training (default: 0.8)
            
        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
                (train_gray, train_color, val_gray, val_color)
            
        Raises:
            ValueError: If the number of color and grayscale images don't match
        """
        color_dir, gray_dir = Path(color_dir), Path(gray_dir)

        # Load color and grayscale images
        color_imgs = ImageUtils.load_images(color_dir, stop_file="999_256.png", img_size=self.img_size)
        gray_imgs = ImageUtils.load_images(gray_dir, stop_file="999_256_bw.png", img_size=self.img_size)

        # Verify that we have matching pairs of images
        if len(color_imgs) != len(gray_imgs):
            raise ValueError(f"Mismatch in number of images: {len(color_imgs)} color images vs {len(gray_imgs)} gray images.")

        # Convert lists to numpy arrays for efficient processing
        color_arr = np.array(color_imgs)
        gray_arr = np.array(gray_imgs)
        
        # Reshape arrays to ensure correct dimensions (batch_size, height, width, channels)
        color_arr = np.reshape(color_arr, (len(color_arr), self.img_size, self.img_size, 3))
        gray_arr = np.reshape(gray_arr, (len(gray_arr), self.img_size, self.img_size, 3))

        # Split dataset into training and validation sets
        split_idx = int(len(color_arr) * train_split)
        self.train_gray = gray_arr[:split_idx]
        self.val_gray = gray_arr[split_idx:]
        self.train_color = color_arr[:split_idx]
        self.val_color = color_arr[split_idx:]

        print(f"Train set : {self.train_color.shape}")
        print(f"Val   set : {self.val_color.shape}")
        
        return self.train_gray, self.train_color, self.val_gray, self.val_color 