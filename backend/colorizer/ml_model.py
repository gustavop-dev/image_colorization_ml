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

    def build_model(self) -> tf.keras.Model:
        # Build the U-Net model for colorization and compile it
        inputs = tf.keras.layers.Input(shape=self.input_shape)

        # Encoder
        d1 = self._down(128, (3, 3), batch_norm=False)(inputs)
        d2 = self._down(128, (3, 3), batch_norm=False)(d1)
        d3 = self._down(256, (3, 3), batch_norm=True)(d2)
        d4 = self._down(512, (3, 3), batch_norm=True)(d3)
        d5 = self._down(512, (3, 3), batch_norm=True)(d4)

        # Decoder + skip connections
        u1 = self._up(512, (3, 3))(d5);  u1 = tf.keras.layers.concatenate([u1, d4])
        u2 = self._up(256, (3, 3))(u1);  u2 = tf.keras.layers.concatenate([u2, d3])
        u3 = self._up(128, (3, 3))(u2);  u3 = tf.keras.layers.concatenate([u3, d2])
        u4 = self._up(128, (3, 3))(u3);  u4 = tf.keras.layers.concatenate([u4, d1])
        u5 = self._up(3,   (3, 3))(u4);  u5 = tf.keras.layers.concatenate([u5, inputs])

        outputs = tf.keras.layers.Conv2D(3, (2, 2), padding="same")(u5)
        self.model = tf.keras.Model(inputs, outputs, name="u-net_colorizer")

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(1e-3),
            loss="mae",
            metrics=["accuracy"],
        )
        return self.model
    
    def colorize(self, image_path: str | Path, save_to: str | Path | None = None) -> np.ndarray:
        """
        Colorize a single grayscale image and optionally save it.

        Args:
            image_path: Path to input grayscale image.
            save_to: Optional path to save the colorized output.

        Returns:
            Colorized image array in uint8 RGB format.
        """
        if self.model is None:
            raise RuntimeError("Modelo no construido.")

        # preprocess the image
        img = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(img_rgb, (self.img_size, self.img_size))
        inp = (img_rgb.astype(np.float32) / 255.0)[None, ...]  # shape (1, H, W, 3)

        # inference
        pred = self.model.predict(inp)[0]          # (H, W, 3), float32
        pred = np.clip(pred * 255.0, 0, 255).astype(np.uint8)

        # Save output if requested
        if save_to is not None:
            Path(save_to).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(save_to), cv2.cvtColor(pred, cv2.COLOR_RGB2BGR))

        return pred

    
    def train(self, epochs: int = 50, batch_size: int = 32) -> tf.keras.callbacks.History:
        """
        Placeholder for model training
        """
        if self.model is None:
            raise RuntimeError("call build_model() first to create the model.")
        if not hasattr(self, "train_gray"):
            raise RuntimeError("Dataset not loaded. Call load_dataset() first.")

        history = self.model.fit(
            self.train_gray, self.train_color,
            validation_data=(self.val_gray, self.val_color),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1,
        )
        return history      