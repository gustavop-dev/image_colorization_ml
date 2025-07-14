import numpy as np
import tensorflow as tf
import keras
import cv2
from keras.layers import MaxPool2D,Conv2D,UpSampling2D,Input,Dropout
from keras.models import Sequential
from keras.preprocessing.image import img_to_array
import os
from tqdm import tqdm
import re
import matplotlib.pyplot as plt
import pathlib as Path
from typing import Tuple, List

class ColorizationModel:
    """
    Class for handling image colorization using a deep learning model.
    This is a simplified placeholder class for development.
    """
    def __init__(self):
        self.model = None
        self.input_shape = (256, 256, 1)  # Default input shape
        self.initialized = False
    
    # Helpers

    @staticmethod
    def _sorted_alphanumeric(files: List[str]) -> List[str]:
        """
        sorts a list of filenames in alphanumeric order. 
        """
        convert = lambda x: int(x) if x.isdigit() else x.lower()
        key = lambda fname: [convert(c) for c in re.split(r'(\d+)', fname)]
        return sorted(files, key=key)

    def _load_images(self, folder: Path, stop_file: str) -> List[np.ndarray]:
        """
        Read, resize, and scale every image until *stop_file* is found.
        """
        images: List[np.ndarray] = []
        files = self._sorted_alphanumeric([f.name for f in folder.iterdir()])

        for fname in tqdm(files, desc=f"Cargando {folder.name}"):
            if fname == stop_file:
                break
            img = cv2.imread(str(folder / fname), cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)            # BGR ➜ RGB
            img = cv2.resize(img, (self.img_size, self.img_size))  
            img = img.astype(np.float32) / 255.0                  
            images.append(img)

        return images

    # Dataset

    def load_dataset(self, color_dir: str | Path, gray_dir: str | Path, train_split: float = 0.8,) -> None:
        """
        Load images and create train/validation arrays.
        """
        color_dir, gray_dir = Path(color_dir), Path(gray_dir)

        color_imgs = self._load_images(color_dir, stop_file="999_256.png")
        gray_imgs = self._load_images(gray_dir, stop_file="999_256_bw.png")

        if len(color_imgs) != len(gray_imgs):
            raise ValueError(f"Mismatch in number of images: {len(color_imgs)} color images vs {len(gray_imgs)} gray images.")

        # turn lists into numpy arrays
        color_arr = np.array(color_imgs)
        gray_arr = np.array(gray_imgs)
        idx = np.random.permutation(len(color_arr))
        color_arr, gray_arr = color_arr[idx], gray_arr[idx]

        # Split train / test
        split_idx = int(len(color_arr) * train_split)
        self.train_gray, self.val_gray = np.split(gray_arr, [split_idx])
        self.train_color, self.val_color = np.split(color_arr, [split_idx])

        print(f"Train set : {self.train_color.shape}")
        print(f"Val   set : {self.val_color.shape}")

    # U‑Net blocks

    @staticmethod
    def _down(filters: int, k: Tuple[int, int], bn: bool = True):
        layer = tf.keras.Sequential([
            tf.keras.layers.Conv2D(filters, k, strides=2, padding="same"),
            tf.keras.layers.BatchNormalization() if bn else tf.keras.layers.Layer(),
            tf.keras.layers.LeakyReLU(),
        ])
        return layer

    @staticmethod
    def _up(filters: int, k: Tuple[int, int], dropout: bool = False):
        seq = tf.keras.Sequential([
            tf.keras.layers.Conv2DTranspose(filters, k, strides=2, padding="same"),
            tf.keras.layers.Dropout(0.2) if dropout else tf.keras.layers.Layer(),
            tf.keras.layers.LeakyReLU(),
        ])
        return seq

    # Model

    def build_model(self):
        """
        Placeholder for model building
        """
        

        self.initialized = True
        return self.model
    
    def colorize(self, image_path, output_path):
        """
        Placeholder for colorization process
        """
        # In a real implementation, this would colorize the image
        # For now, this is just a placeholder
        
        # Create a dummy file or just return the path
        with open(output_path, 'w') as f:
            f.write('Placeholder for colorized image')
        
        return output_path
    
    def train(self, dataset_path, epochs=10, batch_size=32):
        """
        Placeholder for model training
        """
        print(f"[Mock] Training model on {dataset_path} for {epochs} epochs with batch size {batch_size}")
        return True 