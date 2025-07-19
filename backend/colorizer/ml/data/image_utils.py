"""
Image processing utilities for colorization.
"""

import numpy as np
import cv2
from keras.preprocessing.image import img_to_array
from tqdm import tqdm
import re
from pathlib import Path
from typing import Tuple, List

class ImageUtils:
    """
    Utility class for image processing operations.
    """
    
    @staticmethod
    def sorted_alphanumeric(files: List[str]) -> List[str]:
        """
        Sort a list of filenames in alphanumeric order.
        
        This function properly handles filenames with numbers, ensuring that
        'file2.jpg' comes before 'file10.jpg' instead of after it.
        
        Args:
            files (List[str]): List of filenames to sort
            
        Returns:
            List[str]: Sorted list of filenames
        """
        convert = lambda x: int(x) if x.isdigit() else x.lower()
        key = lambda fname: [convert(c) for c in re.split(r'(\d+)', fname)]
        return sorted(files, key=key)

    @staticmethod
    def load_images(folder: Path, stop_file: str, img_size: int) -> List[np.ndarray]:
        """
        Load and preprocess images from a directory.
        
        This method reads images from the specified folder, converts them to RGB,
        resizes them to the model's input size, and normalizes pixel values to [0,1].
        Loading stops when the specified stop_file is encountered.
        
        Args:
            folder (Path): Directory containing images to load
            stop_file (str): Filename to stop loading at (exclusive)
            img_size (int): Size to resize images to
            
        Returns:
            List[np.ndarray]: List of preprocessed image arrays
        """
        images: List[np.ndarray] = []
        files = ImageUtils.sorted_alphanumeric([f.name for f in folder.iterdir()])

        for fname in tqdm(files, desc=f"Loading {folder.name}"):
            if fname == stop_file:
                break
                
            # Load image in BGR format (OpenCV default)
            img = cv2.imread(str(folder / fname), cv2.IMREAD_COLOR)
            
            # Convert BGR to RGB for consistency with matplotlib/tensorflow
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize to model input size
            img = cv2.resize(img, (img_size, img_size))
            
            # Normalize pixel values to [0, 1] range
            img = img.astype(np.float32) / 255.0
            
            # Convert to array format expected by Keras
            images.append(img_to_array(img))

        return images 